# Build ryde_scrape
cd src
zip ryde_scrape.zip ryde_scrape.py
pip3 install --target ./package requests boto3 bs4 datetime
cd package
zip -r ../ryde_scrape.zip .
cd ..
rm -rf ./package
cd ..
mv src/ryde_scrape.zip out/ryde_scrape.zip