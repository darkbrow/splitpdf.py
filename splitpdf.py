import argparse
import os
import sys
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter

def get_base_filename(path):
    return os.path.splitext(os.path.basename(path))[0]

def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def split_pdf_multiple_ranges(input_path, output_dir, ranges, prefix="", suffix="", timestamp=False):
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    base_name = get_base_filename(input_path)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for (start_page, end_page) in ranges:
        if start_page < 1 or end_page > total_pages or start_page > end_page:
            raise ValueError(f"잘못된 범위: {start_page}-{end_page}, 총 페이지 수: {total_pages}")

        writer = PdfWriter()
        for i in range(start_page - 1, end_page):
            writer.add_page(reader.pages[i])

        ts = f"_{get_timestamp()}" if timestamp else ""
        output_filename = f"{prefix}{base_name}_{start_page}-{end_page}{ts}{suffix}.pdf"
        output_path = os.path.join(output_dir, output_filename)
        with open(output_path, "wb") as f:
            writer.write(f)

        print(f"저장 완료: {output_path}")

def split_pdf_by_chunk(input_path, output_dir, chunk_size, prefix="", suffix="", timestamp=False):
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    base_name = get_base_filename(input_path)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for start in range(0, total_pages, chunk_size):
        end = min(start + chunk_size, total_pages)
        writer = PdfWriter()
        for i in range(start, end):
            writer.add_page(reader.pages[i])

        ts = f"_{get_timestamp()}" if timestamp else ""
        output_filename = f"{prefix}{base_name}_{start+1}-{end}{ts}{suffix}.pdf"
        output_path = os.path.join(output_dir, output_filename)
        with open(output_path, "wb") as f:
            writer.write(f)

        print(f"저장 완료: {output_path}")

def parse_ranges(ranges_str):
    ranges = []
    for part in ranges_str.split(","):
        start, end = part.split("-")
        ranges.append((int(start), int(end)))
    return ranges

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="PDF 파일을 페이지 범위 또는 일정 단위로 분할하는 스크립트.\n"
                    "원본 PDF를 지정된 범위 또는 일정한 페이지 단위로 잘라서 새로운 PDF 파일로 저장합니다."
    )
    parser.add_argument("input_pdf", help="원본 PDF 파일 경로")
    parser.add_argument("output_dir", help="분할된 PDF를 저장할 디렉토리")
    parser.add_argument("--ranges", help="페이지 범위 (예: '1-3,4-6,7-10'). 여러 범위를 쉼표로 구분")
    parser.add_argument("--chunk", type=int, help="분할할 페이지 단위 (예: 5). 지정한 단위로 자동 분할")
    parser.add_argument("--prefix", help="저장 파일 이름 접두사 (예: 'part_')", default="")
    parser.add_argument("--suffix", help="저장 파일 이름 접미사 (예: '_v1')", default="")
    parser.add_argument("--timestamp", action="store_true", help="파일 이름에 날짜/시간(YYYYMMDD_HHMMSS) 추가")

    # 인자가 없으면 도움말 출력
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.ranges and args.chunk:
        parser.error("ranges와 chunk는 동시에 사용할 수 없습니다. 하나만 선택하세요.")
    elif args.ranges:
        ranges = parse_ranges(args.ranges)
        split_pdf_multiple_ranges(args.input_pdf, args.output_dir, ranges, args.prefix, args.suffix, args.timestamp)
    elif args.chunk:
        split_pdf_by_chunk(args.input_pdf, args.output_dir, args.chunk, args.prefix, args.suffix, args.timestamp)
    else:
        parser.error("ranges 또는 chunk 중 하나를 반드시 지정해야 합니다.")

