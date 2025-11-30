from flask import (Flask, json, render_template, request, jsonify, redirect, url_for)
from _common._health_check import check_apollo_health
from _workflows._leads import get_leads
from _customer._profile import CustomerProfile

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
customer = None

def paginate_people(data, page=1, page_size=2):

    total_entries = data.get("total_entries", 0)
    people = data.get("people",[])

    # Get the current page of people
    current_page_people = people[:page_size]

    # Return paginated result
    return {
        "page": page,
        "page_size": page_size,
        "total_entries": total_entries,
        "total_pages": (total_entries + page_size - 1) // page_size,  # Ceiling division
        "people": current_page_people,
    }

@app.route("/", methods=["GET", "POST"])
def index():
    global customer
    
    if request.method == "POST":
        customer_input = request.form.get("customer_input")
        customer = CustomerProfile(customer_input)
        return redirect(url_for("profile"))
    
    return render_template("index.html")


@app.route("/profile", methods=["POST", "GET"])
def profile():
    # Extract customer profile
    profile = customer.get_profile()
    return render_template('profile.html', profile=profile)

@app.route("/results", methods=["GET"])
def results():
    # Get the customer input and page number from the query parameters
    profile = customer.get_profile()

    page = int(request.args.get("page", 1))
    page_size = 15  # Define the number of results per page

    # Process the customer input and get leads
    leads = get_leads(profile, page=page, page_size=page_size)

    paginated_data = paginate_people(leads, page=page, page_size=page_size)

    # Render the results page with the paginated data
    return render_template("results.html", data=paginated_data)


if __name__ == "__main__":
    app.run(debug=True)