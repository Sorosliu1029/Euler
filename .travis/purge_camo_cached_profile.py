#!/usr/bin/python3
"""
Purge Camo cached personal profile of Project Euler
"""
import http.client
import binascii
import json
import sys

hmac_part = "f091285d1f7111bb8c37ff67f2386a820cd426b0"
hex_part = "68747470733a2f2f70726f6a65637465756c65722e6e65742f70726f66696c652f536f726f734c69752e706e67"
purged_url = b"https://projecteuler.net/profile/SorosLiu.png"

def purge_camo_cached_image(conn, hmac_part, hex_part):
    conn.request("PURGE", "/{hmac_part}/{hex_part}".format(hmac_part=hmac_part, hex_part=hex_part))
    res_json = conn.getresponse().read()
    res = json.loads(res_json, encoding='utf-8')
    return res['status'] == 'ok'

if __name__ == "__main__":
    assert binascii.hexlify(purged_url).decode("ascii") == hex_part
    conn = http.client.HTTPSConnection("camo.githubusercontent.com")
    result_msg = "Purge succeed" if purge_camo_cached_image(conn, hmac_part, hex_part) else "Purge failed"
    print(result_msg)