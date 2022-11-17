"""Form class declaration."""
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    DateField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
import requests
from datetime import date
from wtforms.fields.html5 import DateField
from wtforms.validators import URL, DataRequired, Email, EqualTo, Length


class StockForm(FlaskForm):
    """Generate Your Graph."""
    
    #THIS IS WHERE YOU WILL IMPLEMENT CODE TO POPULATE THE SYMBOL FIELD WITH STOCK OPTIONS
    #symbol = SelectField("Choose Stock Symbol",[DataRequired()],)
    stock_symbols = requests.get("https://pkgstore.datahub.io/core/nyse-other-listings/other-listed_csv/data/9f38660d84fe6ba786a4444b815b3b80/other-listed_csv.csv")
    content_clear = stock_symbols.content.decode('utf8')
    csvf = content_clear.splitlines()
    selected=[]
            #Fill stock symbol with api
            #("IBM", "IBM"),
            #("GOOGL", "GOOGL"),
    for x in csvf:
        try:
            data = x.split(',',1)
            symbol = data[0]
            selected.append(tuple((symbol,symbol)))
        except IndexError:
            continue
    symbol = SelectField("Choose Stock Symbol",[DataRequired()],
        choices=selected,
    )

    chart_type = SelectField("Select Chart Type",[DataRequired()],
        choices=[
            ("1", "1. Bar"),
            ("2", "2. Line"),
        ],
    )

    time_series = SelectField("Select Time Series",[DataRequired()],
        choices=[
            ("1", "1. Intraday"),
            ("2", "2. Daily"),
            ("3", "3. Weekly"),
            ("4", "4. Monthly"),
        ],
    )

    start_date = DateField("Enter Start Date")
    end_date = DateField("Enter End Date")
    submit = SubmitField("Submit")



