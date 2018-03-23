
Programm scrapping Facebook (Python version 3.5)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**First step: Access to the Facebook API**

These tokens are needed for user authentifications. Credentials can be
generate via Facebook’s Application

-  App_id = **“”**
-  App_secret = **“”**
-  access_token = **App_id + “\|” + App_secret**

**We mainly import the python GraphAPI library**

.. code:: ipython3

    import pandas as pd
    from facepy import GraphAPI
    import openpyxl

**Second step: Retrieve the last imported date**

For that we need to open an excel file with the openpyxl library

.. code:: ipython3

    wb = openpyxl.load_workbook('since_date.xlsx')        
    sheet = wb.get_sheet_by_name('since_date')
    local='A'+str(sheet.max_row)
    since_inp= sheet[local].value  
    since_inp=str(since_inp)

**Third step: Use GraphAPI to retrieve all facebook messages from users
listed in list_url**

.. code:: ipython3

list_url = [
'163293133759468',
'192953374168500',
'262969587120491',
'154409134651718',
'121470551304281',
'12619074644',
'350292144987173',
'192116037510649',
'59627025578',
'527856500606836',
'391396000937067',
'642045892502440',

];

    until_inp =  strftime("%Y-%m-%d")
    since = "since=" + since_inp
    until = "until=" + str(until_inp)
    node = page_id + "/"+"posts?"+ since+"&"+until+"&"
    parameters = "fields=message,created_time&access_token=%s" % ( access_token)
    url = node + parameters
    graph = GraphAPI(access_token)
    i=0
    posts=[]
    for page_id in list_url:
            node = page_id + "/"+"posts?"+ since+"&"+until+"&"
            url = node + parameters
            globals()["datas" + str(i)]=graph.get(url, page=True, retry=5)
            for data in globals()["datas" + str(i)]:
                  posts.append(data)
                  i = i+1

**Forth step: step of data management in order to obtain exploitable
data**

*in posts we obtain a list of list of dictionary ,to access to the data
we can do that, but there is certainly more efficient….*

**step 4-a** Extract key- values ‘data’ from the list of dictionnary
posts

.. code:: ipython3

    posts_data=[d['data'] for d in posts]
    

**step 4-b** Transform list of list of dictionnary into a list of
dictionnary post named message

.. code:: ipython3

    post_message=[]
    i=0
    while i <len(posts)+1: 
        post_message.extend(posts_data[i])
        i =i+1

**step 4-c** Drop all the posts without message keep them in
post_message_only

.. code:: ipython3

    post_message_only=[]
    
    i=0
    while i <len(post_message):
        if (len(post_message[i]) == 3):
            post_message_only.append(post_message[i])
            i =i+1
        else:
            i =i+1

**step 4-d** Transform a list of dictionary into a list of values

.. code:: ipython3

    messages = [[x['id'],x['created_time'],x['message']] for x in post_message_only]

**Fith step: store the message in an excel file**

**step 5-a: Creation of the initial csv file**

Creation of the initial csv file

.. code:: ipython3

    my_df = pd.DataFrame(messages)
    my_df.to_csv('my_csv_file.csv',index=False,header=False)

**step 5-b: Adding column names**

.. code:: ipython3

    df= pd.read_csv('my_csv_file.csv', sep=',', encoding='latin-1')
    df.columns = ['user_id','date_created','message']

**step 5-c: Split user_id into user_id and id_message**

.. code:: ipython3

    i = df.columns.get_loc('user_id')
    df2 = df['user_id'].str.split("_", expand=True)
    df3= pd.concat([df.iloc[:, :i], df2, df.iloc[:, i+1:]], axis=1)
    df3.columns = ['user_id','id_message','date_created','message']
    df3.to_csv('extractfrom'+strftime("%Y-%m-%d")+'.csv',index=False)

**step 5-d: Insert MAJ date in the excel file**

.. code:: ipython3

    wb = openpyxl.load_workbook('since_date.xlsx')
    sheet = wb.get_sheet_by_name('since_date')
    new_date='A'+str(sheet.max_row+1)
    sheet[new_date] = strftime("%Y-%m-%d")
    wb.save('since_date.xlsx')
