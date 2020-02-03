
# How to test:
### import the indexer
`from twit.indexer import *`.    
`ind=IndexManager()`

### import db variable
`from twit.utils import GetMongo_client`.    
`db = GetMongo_client()`.   

### set the indexer     
`from lupyne import engine`.        
`indexer= engine.Indexer()`.         
`indexer.set('usr_name',stored=True) #user name is done`.         
`indexer.set('text',engine.Field.Text) #set the field of user to text.`.        

