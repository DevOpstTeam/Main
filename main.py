""" FastAPI script 

This script creates an API using FastAPI that will interact with a P2000 database.
"""

from fastapi import FastAPI, HTTPException, Depends
from src.schemas.p2000Message import P2000Message as messageSchema
from src.schemas.p2000Message import P2000MessageCreate as messageCreateSchema
from src.models.p2000Message import Meldingen as P2000Message
from src.models.p2000Message import ABP
from src.models.p2000Message import Regio
from src.alchemyDatabase import SessionLocal
from datetime import datetime

app = FastAPI()
default_message = "0 down time cicd werkt!" #returned on "/" endpoint  

def get_db():
    """Get a reference to the database and close the database when finished."""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    """API root endpoint to check if the API is running."""
    return default_message

@app.get("/messages")
def filter_messages(dateStart: str | None = None, dateEnd: str | None = None, timeStart: str | None = None, 
                    timeEnd: str | None = None, abp: str | None = None, priority:int | None = None, 
                    region: str | None = None, capcode: str | None = None, db=Depends(get_db)) -> list[messageSchema]:
    """API endpoint for retrieving messages from the database that conform to the specified filters.
        
    Parameters:
    dataStart: a date from which to show messages.
    dateEnd: a date until which to show messages.
    timeStart: a time from when to show messages.
    timeEnd: a time until which to show messages.
    abp: a string that the message's abp value contains.
    priority: the priority that a message has.
    region: a string that the message's region value contains.
    capcode: a string that the message's capcode contains.

    Returns:
    List of P2000 messages.
    """
    messages = db.query(P2000Message)
    
    try:
        dateFormat = "%d-%M-%Y"
        if dateStart != None:
            startDate = datetime.strptime(dateStart, dateFormat)
            messages = messages.filter(P2000Message.Datum >= startDate)
        if dateStart != None:
            startDate = datetime.strptime(dateStart, dateFormat)
            messages = messages.filter(P2000Message.Datum >= startDate)
        if dateEnd != None:
            endDate = datetime.strptime(dateEnd, dateFormat)
            messages = messages.filter(P2000Message.Datum <= endDate)
        if timeStart != None:
            messages = messages.filter(P2000Message.Tijd > timeStart)
        if timeEnd != None:
            messages = messages.filter(P2000Message.Tijd < timeEnd)
        if abp != None:
            # Check which ABP ID matches the abp query value
            abpTable = db.query(ABP)
            abpID = abpTable.filter(ABP.abp_naam == abp).first().abp_id

            # Filter the messages on the correct abp ID
            messages = messages.filter(P2000Message.abp_id == abpID)
        if priority != None:
            messages = messages.filter(P2000Message.prioriteit == priority)
        if region != None:
            # Check which region ID matches the region query value
            regionTable = db.query(Regio)
            regionId = regionTable.filter(Regio.regio_naam.contains(region)).first().regio_id

            # Filter the messages on the correct region ID
            messages = messages.filter(P2000Message.regio_id == regionId)
        if capcode != None:
            messages = messages.filter(P2000Message.Capcode.contains(capcode))
    except Exception as e:
        print(e)
        return list()
    return messages.all()

@app.post("/messages/", status_code=201)
def create_message(message: messageCreateSchema, db=Depends(get_db)) -> messageSchema:
    """API endpoint for adding a new message to the P2000 database.
    
    Parameters:
    message: the P2000 message you want to add to the database.

    Returns:
    A P2000 message.
    """
    db_message = P2000Message(Datum=message.Datum,
                              Tijd=message.Tijd,
                              ABP=message.ABP,
                              Prioriteit=message.Prioriteit,
                              Regio=message.Regio,
                              Capcode=message.Capcode)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@app.get("/messages/{message_id}")
def read_message(message_id: int, db=Depends(get_db)) -> messageSchema:
    """API endpoint for reading a specific message.
    
    Parameters:
    message_id: the ID of the message you want to return.

    Returns:
    A P2000 message.
    """
    message = db.query(P2000Message).filter(P2000Message.id == message_id).first()
    if message == None:
        raise HTTPException(status_code=404, detail=f'message with ID {message_id} not found')
    return message

@app.delete("/messages/{message_id}", status_code=200)
def delete_message(message_id: int, db = Depends(get_db)):
    """API endpoint for deleting a message for the database.
    
    Parameters:
    message_id: the ID of the message you want to delete from the database.
    """
    message = db.query(P2000Message).filter(P2000Message.id == message_id).first()
    db.delete(message)
    db.commit()

@app.put("/messages/{message_id}")
def update_message(message_id: int, newMessage: messageCreateSchema, db = Depends(get_db)) -> messageSchema:
    """API endpoint for updating a message in the database.
    
    Parameters:
    message_id: the ID of the old message that you want to update.
    newMessage: the message that contains the new information.
    """
    message = db.query(P2000Message).filter(P2000Message.id == message_id)
    message.update({P2000Message.Datum: newMessage.Datum,
                    P2000Message.Tijd: newMessage.Tijd,
                    P2000Message.ABP: newMessage.ABP,
                    P2000Message.Prioriteit: newMessage.Prioriteit,
                    P2000Message.Regio: newMessage.Regio,
                    P2000Message.Capcode: newMessage.Capcode})
    db.commit()
    return message

@app.get("/safest")
def get_safest_region(inverted: bool | None = None, db = Depends(get_db)):
    # Get all the regions & messages
    messages = db.query(P2000Message)
    regions = db.query(Regio)

    # Create a dictionary with every region and the amount of messages for that region
    safestRegions = {regio.regio_naam: 0 for regio in regions.all()}
    # Fill the dictionary
    for region in regions:
        amountOfMessages = len(messages.filter(P2000Message.regio_id == region.regio_id).all())
        safestRegions[region.regio_naam] = amountOfMessages
    
    # Return the sorted dictionary
    sortedRegions = sorted(safestRegions.items(), key=lambda item: item[1])
    if inverted:
        return dict(sortedRegions)
    else:
        return dict(reversed(sortedRegions))