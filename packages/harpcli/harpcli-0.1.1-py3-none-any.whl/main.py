import os
import webbrowser
from typing import List
from uuid import UUID

import requests
import typer

app = typer.Typer()

url_prefix = "v1/buyer"
api_token = os.getenv("API_TOKEN", "")
headers = {"Authorization": f"Bearer {api_token}"}


@app.command()
def add_payment_method():
    typer.echo("Let's add a new payment method.")

    # Let's assume your FastAPI server is running locally on port 8000
    fastapi_url = os.getenv("FASTAPI_URL", "http://localhost:8000")
    ### Add prefix after localhost
    fastapi_url = f"{fastapi_url}/{url_prefix}"

    typer.echo(fastapi_url)

    # Request to generate a new Stripe Payment Method
    response = requests.post(f"{fastapi_url}/create-checkout-session", headers=headers)
    if response.status_code == 200:
        response_json = response.json()

        stripe_payment_url = response_json["data"]

        # Open the Stripe Checkout page
        webbrowser.open(stripe_payment_url)

        # Once the user completes the payment on the Stripe Checkout page, Stripe will redirect them to your specified return_url (you will need to set this up on your FastAPI backend).
        # On the return page, you can retrieve the PaymentMethod ID from the URL parameters and send it back to the FastAPI backend to associate it with the user and save it in the database.
    else:
        typer.echo(response.status_code)
        typer.echo("Something went wrong. It was reported to the devs. Slack us if you need help.")


@app.command()
def order():
    typer.echo("Let's create a new order.")

    # Prompt user for each field
    store_id = None
    while store_id is None:
        store_id_str = typer.prompt("Enter the store_id")
        try:
            store_id = UUID(store_id_str)
        except ValueError:
            typer.echo("Invalid UUID format, please try again.")
    products: List[dict] = []

    # Request the first product ID and quantity
    product_id = typer.prompt("Enter product id")
    quantity = int(typer.prompt(f"Enter quantity for product {product_id}"))
    products.append({"product_id": product_id, "quantity": quantity})

    # For the second and next products, give the option to quit
    while True:
        product_id = typer.prompt("Enter next product id (or 'q' to quit)")
        if product_id.lower() == "q":
            break
        quantity = int(typer.prompt(f"Enter quantity for product {product_id}"))
        products.append({"product_id": product_id, "quantity": quantity})

    # If no products are added, print error message and exit
    if not products:
        typer.echo("You must order at least one product!")
        return

    # Let's assume your FastAPI server is running locally on port 8000
    fastapi_url = os.getenv("FASTAPI_URL", "http://localhost:8000")
    fastapi_url = f"{fastapi_url}/{url_prefix}"

    order_params = {"products": products, "store_id": store_id}

    # Send request to create new order
    response = requests.post(f"{fastapi_url}/order", json=order_params, headers=headers)

    if response.status_code == 201:
        typer.echo("Order created successfully!")
    else:
        typer.echo(response.status_code)
        typer.echo(response.json())
        typer.echo("Something went wrong. It was reported to the devs. Slack us if you need help.")


if __name__ == "__main__":
    app()
