#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter

def parse_page_selection(selection_str, max_page):
    if not selection_str:
        return list(range(1, max_page + 1))
    
    pages = set()
    for part in selection_str.split(','):
        part = part.strip()
        if '-' in part:
            start, end = part.split('-', 1)
            start = int(start.strip())
            end = int(end.strip())
            if start > end or start < 1 or end > max_page:
                raise ValueError(f"Invalid page range: {part}")
            pages.update(range(start, end + 1))
        else:
            page = int(part)
            if page < 1 or page > max_page:
                raise ValueError(f"Invalid page number: {page}")
            pages.add(page)
    
    return sorted(pages)

def cmd_merge(args):
    if len(args.inputs) < 2:
        print("Error: merge requires at least two input PDFs", file=sys.stderr)
        return 1
    
    writer = PdfWriter()
    for input_path in args.inputs:
        try:
            reader = PdfReader(input_path)
            for page in reader.pages:
                writer.add_page(page)
        except Exception as e:
            print(f"Error reading {input_path}: {e}", file=sys.stderr)
            return 1
    
    try:
        with open(args.output, 'wb') as f:
            writer.write(f)
    except Exception as e:
        print(f"Error writing output: {e}", file=sys.stderr)
        return 1
    
    return 0

def cmd_split(args):
    try:
        reader = PdfReader(args.input)
    except Exception as e:
        print(f"Error reading {args.input}: {e}", file=sys.stderr)
        return 1
    
    max_page = len(reader.pages)
    
    if args.every:
        if args.every < 1:
            print("Error: --every must be at least 1", file=sys.stderr)
            return 1
        
        out_dir = Path(args.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        
        for i in range(0, max_page, args.every):
            chunk = reader.pages[i:i + args.every]
            writer = PdfWriter()
            for page in chunk:
                writer.add_page(page)
            
            output_path = out_dir / f"chunk_{i // args.every + 1}.pdf"
            try:
                with open(output_path, 'wb') as f:
                    writer.write(f)
            except Exception as e:
                print(f"Error writing {output_path}: {e}", file=sys.stderr)
                return 1
        
        return 0
    
    if not args.pages:
        print("Error: --pages is required when not using --every", file=sys.stderr)
        return 1
    if not args.output:
        print("Error: -o/--output is required with --pages", file=sys.stderr)
        return 1
    
    try:
        pages = parse_page_selection(args.pages, max_page)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    writer = PdfWriter()
    for page_num in pages:
        writer.add_page(reader.pages[page_num - 1])
    
    try:
        with open(args.output, 'wb') as f:
            writer.write(f)
    except Exception as e:
        print(f"Error writing output: {e}", file=sys.stderr)
        return 1
    
    return 0

def cmd_rotate(args):
    try:
        reader = PdfReader(args.input)
    except Exception as e:
        print(f"Error reading {args.input}: {e}", file=sys.stderr)
        return 1
    
    max_page = len(reader.pages)
    
    if args.pages:
        try:
            pages = parse_page_selection(args.pages, max_page)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    else:
        pages = list(range(1, max_page + 1))
    
    writer = PdfWriter()
    for i, page in enumerate(reader.pages, start=1):
        if i in pages:
            page.rotate(args.angle)
        writer.add_page(page)
    
    try:
        with open(args.output, 'wb') as f:
            writer.write(f)
    except Exception as e:
        print(f"Error writing output: {e}", file=sys.stderr)
        return 1
    
    return 0

def main():
    parser = argparse.ArgumentParser(
        prog='pdf_forge',
        description='PDF manipulation tool',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Merge subcommand
    merge_parser = subparsers.add_parser('merge', help='Merge multiple PDFs into one')
    merge_parser.add_argument('inputs', nargs='+', help='Input PDF files')
    merge_parser.add_argument('-o', '--output', required=True, help='Output PDF file')
    merge_parser.set_defaults(func=cmd_merge)

    # Split subcommand
    split_parser = subparsers.add_parser('split', help='Split a PDF into pages or chunks')
    split_parser.add_argument('input', help='Input PDF file')
    split_parser.add_argument('--pages', help='Page selection (e.g., "1-3,5")')
    split_parser.add_argument('--every', type=int, help='Write one PDF per N pages')
    split_parser.add_argument('--out-dir', default='.', help='Output directory for chunks')
    split_parser.add_argument('-o', '--output', help='Output file for selected pages')
    split_parser.set_defaults(func=cmd_split)

    # Rotate subcommand
    rotate_parser = subparsers.add_parser('rotate', help='Rotate pages in a PDF')
    rotate_parser.add_argument('input', help='Input PDF file')
    rotate_parser.add_argument('--angle', type=int, choices=[90, 180, 270], required=True,
                               help='Rotation angle (90, 180, or 270)')
    rotate_parser.add_argument('--pages', help='Page selection (e.g., "1-3,5")')
    rotate_parser.add_argument('-o', '--output', required=True, help='Output PDF file')
    rotate_parser.set_defaults(func=cmd_rotate)

    args = parser.parse_args()
    sys.exit(args.func(args))

if __name__ == '__main__':
    main()
