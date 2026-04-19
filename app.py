from flask import Flask, render_template, request
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

app = Flask(__name__)

data = pd.read_csv("ambition_box.csv")



@app.route("/")
def home():
    location = data["location"].unique()
    about = data["about"].unique()
    ratings = data["ratings"].unique()

    return render_template("index.html", location = location ,about = about, ratings = ratings)
                           


@app.route("/search", methods=["POST"])
def search():
    location = request.form.get("location")
    about = request.form.get("about")
    ratings = request.form.get("ratings")
    output = request.form.get("output")

    filtered_data = data

    if location:
        filtered_data = filtered_data[filtered_data["location"] == location]

    if about:
        filtered_data = filtered_data[filtered_data["about"] == about]

    if ratings:
        filtered_data["ratings"] = pd.to_numeric(filtered_data["ratings"], errors='coerce')
        filtered_data = filtered_data[filtered_data["ratings"] >= float(ratings)]

    if output == "Visualization":
        filtered_data["salaries"] = pd.to_numeric(filtered_data["salaries"], errors='coerce')
        filtered_data["jobs"] = pd.to_numeric(filtered_data["jobs"], errors='coerce')
        filtered_data["reviews"] = pd.to_numeric(filtered_data["reviews"], errors='coerce')
        filtered_data["ratings"] = pd.to_numeric(filtered_data["ratings"], errors='coerce')


        if filtered_data.empty:
            return render_template("search.html",message="No Data Found")
        
        plt.figure(figsize=(8,5))
        filtered_data[["salaries","jobs","reviews","ratings"]].plot()
        plt.title("Trend of Job Data")
        plt.xlabel("index")
        plt.ylabel("values")
        plt.grid(True)
        plt.savefig("static/line.png")
        plt.close()


        plt.figure(figsize=(7,4))
        filtered_data.head(10)[["salaries","jobs","reviews","ratings"]].plot(kind='bar', width=0.7)
        plt.title("Top 10 Records")
        plt.xlabel("index")
        plt.ylabel("values")
        plt.xticks(rotation=0,fontsize=8)
        plt.yticks(fontsize=8)
        plt.savefig("static/bar.png")
        plt.close()



        plt.figure(figsize=(8,5))
        filtered_data[["salaries","jobs","reviews","ratings"]].plot(kind="hist",bins=10)
        plt.title("Data Distribution")
        plt.xlabel("index")
        plt.ylabel("values")
        plt.savefig("static/hist.png")
        plt.close()


        plt.figure(figsize=(5,5))
        filtered_data[["salaries","jobs","reviews","ratings"]].mean().plot(kind='pie',autopct='%1.1f%%')
        plt.title("Average Distribution")
        plt.savefig("static/pie.png")
        plt.close()
        return render_template("search.html", show_graph=True)
    else:
        return render_template("search.html",tables=filtered_data.values,titles=filtered_data.columns, show_graph=False)




if __name__ == "__main__":
    app.run(debug=True)