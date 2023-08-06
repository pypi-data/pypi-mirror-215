import argparse
import datetime
import ipaddress
import math
import os

import matplotlib.pyplot as plt
import pandas as pd
import pygeoip
import report
from alert import BotnetAlert, ExfiltrationAlert
from scipy.stats import norm

alerts = {}

if not os.path.exists("images"):
    os.mkdir("images")


def printq(*args):
    if not arguments.quiet:
        print(*args)


def dataExfiltration(percentage):
    printq(
        f"[!] IPs above the {percentage} percentile of the downloads over uploads in this session.\n"
    )

    percentage = int(percentage)

    # Calculate the total downloaded and uploaded bytes per IP
    ratios = data.groupby(["src_ip"], as_index=False)[["down_bytes", "up_bytes"]].sum()

    # Calculate the ratio between downloaded and uploaded bytes
    ratios["ratio"] = ratios[["down_bytes", "up_bytes"]].mean(axis=1)

    # Calculate the z-score for the ratio
    ratios["z_score"] = (ratios["ratio"] - ratios["ratio"].mean()) / ratios[
        "ratio"
    ].std()

    # Calculate the z-score threshold based on the desired percentage
    z_score_threshold = math.ceil((norm.ppf(percentage / 100)))

    # Outlier traffic. Above the average percentage defined by user
    outliers = ratios[ratios["z_score"] > z_score_threshold]

    printq(outliers.sort_values(["ratio"], ascending=False))

    for (
        _,
        row,
    ) in outliers.iterrows():
        alerts.setdefault("exfiltrations", []).append(
            ExfiltrationAlert(
                down_byte=row.down_bytes,
                up_byte=row.up_bytes,
                percentage=percentage,
                addr=row.src_ip,
            )
        )


def botnet(subnet):
    printq(
        f"[!] Flows between internal host to common destinations in the same subnet ({subnet}), may indicate the existance of a internal botnet.\n"
    )

    subnet = ipaddress.IPv4Network(subnet)

    # Filter to src_ip for desired subnet
    same_subnet = data
    same_subnet["src_ip"] = same_subnet["src_ip"].astype(str)

    # Filter to src_ip and dst_ip in the same desired subnet
    same_subnet = same_subnet.loc[
        (data["src_ip"].apply(lambda x: ipaddress.IPv4Address(x) in subnet))
        & (data["dst_ip"].apply(lambda x: ipaddress.IPv4Address(x) in subnet))
    ]

    # Associates each dst_ip with a set of IPs and a set of timestamps
    same_subnet = same_subnet.groupby(["dst_ip"], as_index=False).agg(
        {"src_ip": list, "timestamp": list}
    )

    # Calculate the frequency of the communications
    def frequency(comms, period):
        return len(comms) / (period[-1] - period[0])

    same_subnet["frequency"] = same_subnet.apply(
        lambda x: frequency(x.src_ip, x.timestamp), axis=1
    )

    # Clean non relevant series
    same_subnet = same_subnet.drop(["timestamp"], axis=1)

    # Clean repeated IPs
    same_subnet["src_ip"] = same_subnet["src_ip"].apply(lambda x: list(set(x)))

    # Order
    same_subnet = same_subnet.sort_values(["frequency"], ascending=False)

    printq(same_subnet)

    for (
        _,
        row,
    ) in same_subnet.iterrows():
        alerts.setdefault("botnet", []).append(
            BotnetAlert(
                subnet=str(subnet),
                peers=row.src_ip,
                frequency=row.frequency,
                addr=row.dst_ip,
            )
        )


def countryVolume():
    printq(
        f"[!] Calculate the country of origin of the destion IPs and the connection volume for each country. Generating a PNG with the bar graph.\n"
    )

    gi = pygeoip.GeoIP("./sentinel/GeoIP_DBs/GeoIP.dat")

    # Analyse of destination countries connection volume
    countries = data
    countries["country"] = countries["dst_ip"].apply(
        lambda ip: gi.country_code_by_addr(ip)
    )
    volume = (
        countries.groupby(["country"])["dst_ip"].count().sort_values(ascending=False)
    )

    printq(volume)

    # Generates bar chart image
    countries = [x if x != "" else "Unknown" for x in volume.index]
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.barh(countries, volume.values)
    ax.set_xlabel("Country")
    ax.set_ylabel("Number of connection")

    for i, v in enumerate(volume):
        ax.text(v, i, str(v), va="center")

    ax.set_title("Number of connection per country")

    filepath = "images/volumexcountry"
    fig.savefig(fname=filepath)

    return f"""
# Connection volume by country

The correlation between connection volume and country of destination can be viewed in the graphic bellow.

![Volumebycountry]({filepath}.png)

"""

def trafficDistribution():
    traffic = data    
    traffic['hour'] = pd.to_datetime(traffic['timestamp'] / 100.0, unit='s').dt.hour
    hourly = traffic['hour'].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(hourly.index,hourly.values)
    ax.set_xlabel("Hours")
    ax.set_ylabel("Number of connections")
    ax.set_title("Connections per hour during a day")
    ax.set_xticks(range(24))
    
    filepath = "images/connectionsxhour"
    fig.savefig(fname=filepath)

    printq(hourly)

    return f"""
# Connection volume per hour

This graph ilustrates the number of connection per hour during a day

![Connectionsperhout]({filepath}.png)

"""
    
    
def main():
    global data
    data = pd.read_parquet(arguments.data)

    intro = f"""# Sentinel traffic report

This report was automatically generated at **{str(datetime.datetime.utcnow())}** by the **Sentinel** service.
"""

    # Clean operations
    operations = dict(arguments._get_kwargs())
    del operations["data"]
    del operations["quiet"]
    del operations["pdf"]

    for key, value in list(operations.items()):
        if value:
            value = f'"{value}"' if value and value != True else ''            
            func = f"{key}({value})"
            printq()
            r = eval(func)
            if r:
                intro += r

    # Print results to pdf
    if dict(arguments._get_kwargs())["pdf"]:
        report.printReport(alerts, intro)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Traffic analysis tool.")
    parser.add_argument(
        "--data", type=str, help="Path to datafile to analyze", required=True
    )

    parser.add_argument(
        "-dx",
        "--dataExfiltration",
        type=int,
        help="Threshold percentage for outliers in upload/download byte amount",
    )

    parser.add_argument(
        "-bn",
        "--botnet",
        type=str,
        help="Detecting possible botnet communication in specified networks, or all networks",
    )

    parser.add_argument(
        "-cv",
        "--countryVolume",
        action="store_true",
        help="Measures the connection volume per country",
    )

    parser.add_argument(
        "-td",
        "--trafficDistribution",
        action="store_true",
        help="Generates a graph ilustrating the hourly distribution of the volume of connections during a day",
    )

    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress stdout")

    parser.add_argument("-p", "--pdf", action="store_true", help="Export to PDF file")

    global arguments
    arguments = parser.parse_args()

    main()
