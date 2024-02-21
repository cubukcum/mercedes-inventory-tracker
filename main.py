import requests
import json
import smtplib
import time
import os
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def getAvailableCarsFirst():
    # Define the URL and parameters
    url = "https://shop.mercedes-benz.com/smsc-backend-os/dcp-api//v2/market-tr/products/search"
    newurl = "https://ap.api.oneweb.mercedes-benz.com/commerce/ocb/dcp-api/v2/market-tr/products/search"

    #url = "https://shop.mercedes-benz.com/smsc-backend-os/dcp-api//v2/market-tr/products/search?query=:price-asc:allCategories:market-tr-new-passenger-cars:model:E-SERISI:bodyType:LIMOUSINE&currentPage=0&pageSize=12&fields=FULL&lang=tr"
    params = {
        "query": ":price-asc:allCategories:market-tr-new-passenger-cars:model:E-SERISI:bodyType:LIMOUSINE",
        "currentPage": "0",
        "pageSize": "12",
        "fields": "FULL",
        "lang": "tr"
    }

    # Define headers
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://www.mercedes-benz.com.tr",
        "Referer": "https://www.mercedes-benz.com.tr/passengercars/buy/new-car/search-results.html/?emhvehicleAssortment=new-passenger-cars&emhsort=price-asc&ct=null&emhmodel=E-SERISI&emhbodyType=LIMOUSINE",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

    # Send the GET request
    response = requests.get(newurl, params=newparams, headers=newheaders)

    # Check the response status code
    if response.status_code == 200:
        # The response content contains the data you are looking for
        data = response.json()

        # Create or open the "cars.txt" file for writing
        with open("oldCars.txt", "w") as cars_file:
            # Iterate through products and write information to the file
            if data.get("products"):
                for product in data["products"]:
                    model_description = product.get("description", "")
                    model_year = product.get("modelYear", "")
                    fuel_type = product.get("fuelType", {}).get("name", "")
                    list_price = product.get("listPrice", {}).get("formattedValue", "")
                    fuel_economy = json.loads(product.get("localEmissionAndConsumptionData", "{}")).get("uidata", {}).get("attributes", [{}])[0].get("value", "")

                    stock_info = product.get("stock", {})
                    estimated_arrival_date = stock_info.get("estimatedArrivalDate", "")
                    stock_level_status = stock_info.get("stockLevelStatus", "")
                    stock_type = stock_info.get("stockType", "")

                    output_text = f"Model Description: {model_description}\n"
                    output_text += f"Model Year: {model_year}\n"
                    output_text += f"Fuel Type: {fuel_type}\n"
                    output_text += f"List Price: {list_price}\n"
                    output_text += f"Fuel Economy: {fuel_economy}\n"
                    output_text += f"Stock Information:\n"
                    output_text += f"  Estimated Arrival Date: {estimated_arrival_date}\n"
                    output_text += f"  Stock Level Status: {stock_level_status}\n"
                    output_text += f"  Stock Type: {stock_type}\n\n"
                    output_text += "************************************************\n"

                    # Write the product information to the file
                    cars_file.write(output_text)

        print("Data saved to 'oldCars.txt' file for the first time")
    else:
        print("response error start")
        print(response.content)
        print(f"Request failed with status code: {response.status_code}")
        print("respenso error end")

getAvailableCarsFirst()

def getAvailableCars():
    # Define the URL and parameters
    url = "https://shop.mercedes-benz.com/smsc-backend-os/dcp-api//v2/market-tr/products/search"
    #url = "https://shop.mercedes-benz.com/smsc-backend-os/dcp-api//v2/market-tr/products/search?query=:price-asc:allCategories:market-tr-new-passenger-cars:model:E-SERISI:bodyType:LIMOUSINE&currentPage=0&pageSize=12&fields=FULL&lang=tr"
    params = {
        "query": ":price-asc:allCategories:market-tr-new-passenger-cars:model:E-SERISI:bodyType:LIMOUSINE",
        "currentPage": "0",
        "pageSize": "12",
        "fields": "FULL",
        "lang": "tr"
    }

    # Define headers
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://www.mercedes-benz.com.tr",
        "Referer": "https://www.mercedes-benz.com.tr/passengercars/buy/new-car/search-results.html/?emhvehicleAssortment=new-passenger-cars&emhsort=price-asc&ct=null&emhmodel=E-SERISI&emhbodyType=LIMOUSINE",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

    # Send the GET request
    response = requests.get(url, params=params, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # The response content contains the data you are looking for
        data = response.json()

        # Create or open the "cars.txt" file for writing
        with open("newCars.txt", "w") as cars_file:
            # Iterate through products and write information to the file
            if data.get("products"):
                for product in data["products"]:
                    if product.get("modelYear") == "2024":
                        send_email_urgent()
                
                    model_description = product.get("description", "")
                    model_year = product.get("modelYear", "")
                    fuel_type = product.get("fuelType", {}).get("name", "")
                    list_price = product.get("listPrice", {}).get("formattedValue", "")
                    fuel_economy = json.loads(product.get("localEmissionAndConsumptionData", "{}")).get("uidata", {}).get("attributes", [{}])[0].get("value", "")

                    stock_info = product.get("stock", {})
                    estimated_arrival_date = stock_info.get("estimatedArrivalDate", "")
                    stock_level_status = stock_info.get("stockLevelStatus", "")
                    stock_type = stock_info.get("stockType", "")

                    output_text = f"Model Description: {model_description}\n"
                    output_text += f"Model Year: {model_year}\n"
                    output_text += f"Fuel Type: {fuel_type}\n"
                    output_text += f"List Price: {list_price}\n"
                    output_text += f"Fuel Economy: {fuel_economy}\n"
                    output_text += f"Stock Information:\n"
                    output_text += f"  Estimated Arrival Date: {estimated_arrival_date}\n"
                    output_text += f"  Stock Level Status: {stock_level_status}\n"
                    output_text += f"  Stock Type: {stock_type}\n\n"
                    output_text += "************************************************\n"

                    # Write the product information to the file
                    cars_file.write(output_text)

        print("Data saved to 'newCars.txt' file to check differences")
    else:
        print(f"Request failed with status code: {response.status_code}")


# Function to send an email notification
def send_email_urgent():
    subject = "Check the website!"
    message = "New cars in the inventory"
    # Configure your email settings
    sender_email = "your@gmail.com"
    sender_password = "yourpassword"
    receiver_email = "receiver@gmail.com"

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Connect to the SMTP server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, sender_password)

        subject = subject.encode("utf-8")
        message = message.encode("utf-8")

        server.sendmail(sender_email, receiver_email, f"Subject: {subject}\n\n{message}")

def send_email():
    message = "Please check the attachment"
    file_path = "oldCars.txt"
    # Configure your email settings
    sender_email = "your@gmail.com"
    sender_password = "yourpassword"
    receiver_email = "receiver@gmail.com"

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Create a multipart message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Changes in stocks"

    # Attach the message text
    msg.attach(MIMEText(message, "plain"))

    # Attach the text file
    with open(file_path, "rb") as file:
        part = MIMEApplication(file.read(), Name="attachment.txt")

    # Add the attachment to the email
    part["Content-Disposition"] = f'attachment; filename="{file_path}"'
    msg.attach(part)

    # Connect to the SMTP server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())


while True:
    try:
        getAvailableCars()
        with open("oldCars.txt", "r") as f1, open("newCars.txt", "r") as f2:
                # Read the contents of both files
                file1_content = f1.read()
                file2_content = f2.read()


                # Check if the data has changed
                if file1_content != file2_content:
                    print("Files are different, will send an email")
                    # Save the new data to "cars.txt"
                    with open("oldCars.txt", "w") as f1:
                        f1.write(file2_content)
                    # Send an email notification
                    send_email()
        file_path = "newCars.txt"
        if os.path.exists(file_path):
            # Attempt to delete the file
            try:
                os.remove(file_path)
                print(f"{file_path} has been deleted.")
            except Exception as e:
                print(f"An error occurred while deleting {file_path}: {str(e)}")
        else:
            print(f"{file_path} does not exist.")


        # Sleep for 5 minutes
        time.sleep(300)

    except Exception as e:
        # Handle exceptions here, e.g., log the error
        print(f"An error occurred: {str(e)}")
