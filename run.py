import uvicorn

from cleaner_uploader.uploader import main as upload
from csv_generator.csv_generator import generate_orders, write_csv


def main():
    print("1/3 Generating CSV...")
    path = write_csv(generate_orders())
    print(f"    CSV generated at {path}")

    print("2/3 Cleaning and uploading to SQLite...")
    upload()

    print("3/3 Starting API at http://127.0.0.1:8000")
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()