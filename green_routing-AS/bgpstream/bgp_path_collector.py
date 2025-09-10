import pybgpstream
import csv
import pytricia
import json
from concurrent.futures import ProcessPoolExecutor
import os
from concurrent.futures import as_completed
from tqdm import tqdm

def read_json(jsonfilename):
    with open(jsonfilename, 'r') as jsonfile:
        return json.load(jsonfile)


def sanitize_filename(prefix):
    return prefix.replace('/', '_')


def create_bogons_trees(filename1, filename2):
    def populate_pytricia(filename, ipv6=False):
        pyt = pytricia.PyTricia(128) if ipv6 else pytricia.PyTricia()
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader), next(reader)
            for row in reader:
                pyt.insert(row[0], 'bogus')
        return pyt

    return populate_pytricia(filename1), populate_pytricia(filename2, ipv6=True)


def pytricia_to_dict(pytricia_obj):
    return {key: pytricia_obj[key] for key in pytricia_obj.keys()}


def dict_to_pytricia(data, ipv6=False):
    pyt = pytricia.PyTricia(128) if ipv6 else pytricia.PyTricia()
    for key, value in data.items():
        pyt.insert(key, value)
    return pyt


def is_valid(prefix, bogons_pyt_v4, bogons_pyt_v6):
    if bogons_pyt_v4.has_key(prefix) or bogons_pyt_v6.has_key(prefix):
        return False
    leftmost, rightmost = prefix.split('/')
    rightmost = int(rightmost)
    return (':' in leftmost and rightmost <= 64) or (8 <= rightmost <= 24)


def remove_prepending(seq):
    if not seq:
        return []
    result = [seq[0]]  # Start with the first element
    for i in range(1, len(seq)):
        if seq[i] != seq[i - 1]:  # Add to result only if different from the previous element
            result.append(seq[i])
    return result


def has_cycle(seq):
    return len(seq) != len(set(seq))


def collect_bgp_ribs(bogons_pyt_v4_dict, bogons_pyt_v6_dict, date):
    # Reconstruct PyTricia objects inside the worker
    bogons_pyt_v4 = dict_to_pytricia(bogons_pyt_v4_dict)
    bogons_pyt_v6 = dict_to_pytricia(bogons_pyt_v6_dict, ipv6=True)

    stream = pybgpstream.BGPStream(from_time=f"{date} 00:00:00",
                                   until_time=f"{date} 00:00:00 UTC",
                                   projects=['ris'], record_type="ribs")

    output_file = "./ribs/" + date + "_ribs.csv"

    with open(output_file, 'a+', newline='') as f:
        writer = csv.writer(f, delimiter='|')
        for elem in stream:
            row = str(elem).split('|')
            if '{ ' in row:
                continue
            record_type, rec_type, _, _, _, _, _, peer_asn, _, prefix, _, as_path, *_ = row
            if record_type == "rib" and rec_type == "R" and is_valid(prefix, bogons_pyt_v4, bogons_pyt_v6):
                as_path_list = remove_prepending(as_path.split())
                if not has_cycle(as_path_list) and len(as_path_list) > 1:
                    writer.writerow(row)


if __name__ == "__main__":
    # We hold two pytricia trees with bogus IPv4 and IPv6 for filtering
    filename1 = '../cymru/fullbogons-ipv4.txt'
    filename2 = '../cymru/fullbogons-ipv6.txt'
    bogons_pyt_v4, bogons_pyt_v6 = create_bogons_trees(filename1, filename2)
    # Convert PyTricia objects to dictionaries for serialization
    bogons_pyt_v4_dict = pytricia_to_dict(bogons_pyt_v4)
    bogons_pyt_v6_dict = pytricia_to_dict(bogons_pyt_v6)

    # Collection dates for snapshots
    date = "2025-05-01"
    collect_bgp_ribs(bogons_pyt_v4_dict, bogons_pyt_v6_dict, date)
    
            
