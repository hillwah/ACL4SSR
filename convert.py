#!/usr/bin/env python3
import sys
import re

def convert(source_path, dest_path):
    """将 clash.yaml 中的 DOMAIN 条目转换为 Apple.list 格式"""
    domains = []
    in_payload = False

    with open(source_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip() == 'payload:':
                in_payload = True
                continue
            if in_payload:
                # 解析 "- DOMAIN,<domain>" 格式
                match = re.match(r'\s*-\s*DOMAIN,([^\s]+)', line)
                if match:
                    domains.append(match.group(1))
                # 遇到不以 "-" 开头的非空行，说明 payload 部分结束
                elif line.strip() and not line.startswith('-'):
                    break

    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write("# Adobe block rules (generated from a-dove-is-dumb)\n")
        f.write(f"# Last update: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')} UTC\n")
        for domain in domains:
            f.write(f"DOMAIN,{domain}\n")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python convert.py <source_clash.yaml> <output.list>")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
