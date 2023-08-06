

# async def generate_html():
#     await asyncio.sleep(1)  # Simulated loading delay
#     title = 'Dynamic Web Page'
#     css = 'styles.css'
#     js = 'script.js'
#     div_content = '<h1>Welcome to my dynamic web page!</h1><p>Loaded asynchronously.</p>'

#     template = str(components)

#     html_content = template.format(title=title, css=css, js=js, div_content=div_content)

#     # Write the generated HTML content to a file
#     with open('auto.html', 'w') as file:
#         file.write(html_content)

#     return html_content



# @app.route('/auto')
# async def auto():
#     html_content = await generate_html()
#     return html_content


# @app.route('/markets')
# def stock_page():
#     return render_template('markets.html')

# @app.route('/stock_commands')
# def stock_commands():
#     return render_template('stock_commands.html')

# @app.route("/mosh")
# def mosh():
#     return render_template('mosh.html')

# @app.route("/snippets")
# def snippets():
#     return render_template('snippets.html')



# @app.route("/about")
# def about():
#     return render_template('about.html')

# @app.route("/api")
# def api():
#     return render_template('api.html')

# @app.route("/snip")
# def snip():
#     return render_template('snip.html')

# @app.route('/test')
# def test():
#     return render_template('test_scripts.html', helpers=helpers, rest_api=rest_api)

# @app.route("/dropdowns")
# def dropdowns():
#     return render_template('dropdowns.html')

# @app.route("/fetch_and_render", methods=["POST", "GET"])
# async def fetch_and_render():
#     ticker = request.form.get('ticker')
#     if not ticker:
#         return "Missing ticker parameter", 400  # or render a template that displays an error

#     volume_analysis = await webull.get_webull_vol_analysis_data(ticker)

#     avg_price = volume_analysis.avePrice
#     buy_volume = float(volume_analysis.buyVolume)
#     neutral_volume = float(volume_analysis.nVolume)
#     sell_volume = float(volume_analysis.sellVolume)
#     total_volume = float(volume_analysis.totalVolume)

#     volume_analysis_dict = { 
#         'Average Trade Price': avg_price,
#         'Buy Volume': buy_volume,
#         'Neutral Volume': neutral_volume,
#         'Sell Volume': sell_volume,
#         'Total Volume': total_volume
#     }

#     return render_template("api.html", volume_analysis=volume_analysis_dict)




# @app.route("/submit", methods=["POST", "GET"])
# async def submit_form():
#     if request.method == "POST":
#         if request.is_json:
#             json_data = request.get_json()
#             ticker = json_data["ticker"]
#         else:
#             ticker = request.form["ticker"]

#         *market_data, = await get_webull_data(ticker)

#         result_data = {}

#         if market_data is not None and market_data[0]:
#             result_data["Stock Data"] = market_data[0]

#         if market_data is not None and market_data[1]:
#             result_data["Volume Analysis"] = market_data[1]

#         if market_data is not None and market_data[2]:
#             result_data["Financials"] = market_data[2]

#         if market_data is not None and market_data[3]:
#             result_data["Cash Flow"] = market_data[3]

#         if market_data is not None and market_data[4]:
#             result_data["Balance Sheet"] = market_data[4]

#         if market_data is not None and market_data[5]:
#             result_data["Capital Flow"] = market_data[5]

#         if market_data is not None and market_data[6]:
#             result_data["Institutional Ownership"] = market_data[6]

#         if market_data is not None and market_data[7]:
#             result_data["Analyst Ratings"] = market_data[7]

#         if market_data is not None and market_data[8]:
#             result_data["Short Interest"] = market_data[8]


#         if request.is_json:
#             return jsonify(result_data.get("Stock Data", {}))
#         else:
#             return render_template("dropdowns.html", result_data=result_data)
