#!/bin/bash
# Test Examples for File Downloader

echo "=================================="
echo "File Downloader Test Examples"
echo "=================================="
echo ""

echo "Test 1: Show help"
echo "Command: python downloader.py --help"
echo ""
python downloader.py --help
echo ""
echo "Press Enter to continue..."
read

echo "=================================="
echo "Test 2: Download a small test file"
echo "Command: python downloader.py https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
echo ""
python downloader.py https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf
echo ""
echo "Press Enter to continue..."
read

echo "=================================="
echo "Test 3: Download with custom filename"
echo "Command: python downloader.py https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf -o my_test.pdf"
echo ""
python downloader.py https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf -o my_test.pdf
echo ""
echo "Press Enter to continue..."
read

echo "=================================="
echo "Test 4: Download to custom directory"
echo "Command: python downloader.py https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf -d test_downloads"
echo ""
python downloader.py https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf -d test_downloads
echo ""

echo "=================================="
echo "All tests completed!"
echo "Check the 'downloads' and 'test_downloads' folders for downloaded files"
echo "=================================="
