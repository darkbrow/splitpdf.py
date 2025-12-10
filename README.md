# PDF Splitter Script

이 스크립트는 PyPDF2 라이브러리를 활용하여 PDF 파일을 원하는 페이지 범위 또는 일정한 단위(chunk) 로 분할하여 새로운 PDF 파일로 저장합니다.파일 이름에 접두사(prefix), 접미사(suffix), 그리고 타임스탬프(timestamp)를 추가할 수 있습니다.

## 주요 기능

- 페이지 범위 분할: 예를 들어 1-3,4-6 과 같이 지정된 범위별로 PDF를 분할.

- 단위(chunk) 분할: 지정한 페이지 단위(예: 5페이지씩)로 PDF를 자동 분할.

- 파일 이름 옵션:

    * 접두사(prefix)

    * 접미사(suffix)

    * 타임스탬프(YYYYMMDD_HHMMSS)

## 사용법

1. 기본 실행
```
python split_pdf.py input.pdf output_dir --ranges "1-3,4-6"
```
input.pdf: 원본 PDF 파일 경로

output_dir: 분할된 PDF 저장 디렉토리

--ranges: 페이지 범위 지정 (쉼표로 구분)

2. Chunk 단위 분할
```
python split_pdf.py input.pdf output_dir --chunk 5
```
PDF를 5페이지 단위로 자동 분할합니다.

3. 파일 이름 옵션
```
python split_pdf.py input.pdf output_dir --ranges "1-3" --prefix "part_" --suffix "_v1" --timestamp
```

결과 파일 이름 예시:

part_input_1-3_20251211_0351_v1.pdf

## 필요 라이브러리

- Python 3.x

- PyPDF2

- 설치:
```
pip install PyPDF2
```