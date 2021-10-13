# Import libraries
import pandas as pd
import twint
import nest_asyncio
nest_asyncio.apply()

# To expanding the display of text columns
pd.options.display.max_columns = 100

# To configure
c = twint.Config()
c.Search = "SquidGames"
c.Lang = "en"
c.Limit = 50000
c.Since = "2019-01-01"
c.Store_csv = True
c.Output = "./data/tweets_scraped.csv"

# To run the twint
twint.run.Search(c)

# To make a dataframe
data = pd.read_csv('./data/tweets_scraped.csv')
