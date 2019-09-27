# Movie Theater Seating Challenge

## Assumptions
- seatingservice is the service designed to assign seats.
- Writing to file with empty results if no vacant seats for a request are found
- Assuming the seat numbers are combination of str and int for the sake of simplicity and sequence from 1 to 20 etc are sequential
 
## Instructions for setting up repo and executing scripts
- cd seatingservice
- python3  -m virtualenv env
- source env/bin/activate
- pip install -r requirements.txt
- python seatingservice/seat_assignment_script.py /tmp/sampel.txt
	- It outputs name of the file containing results in the last line printed onto console. Ex: "Responses can be found at /home/hamley/PycharmProjects/seatingservice/responses.txt"
- To run tests
	- python -m unittest discover -s tests -p *tests.py
## SOME DESIGN CONSIDERATIONS
- Project is structured in a way that a server/HTTP Framework can be introduced with minimal efforts 
- Avoid duplicacy. So if changes wrt a piece of behaviour is needed. It needs changes at only one location
- Small stateless functions wherever possible
- Seperation of responsibilities -> Each function has single responsibility wherever possible
- Can be evolved to support more usecases
- Each line in the requests file is treated as event, and an event processor processes these events, so that this can be extended to a more realistic use case like reading from a consumer(Kafka) maybe
- The eventsprocessor can be evolved into a cleaner rule engine based on the type of events ( to support mulitple events) with minimal efforts
- The requirement of writing results to file is modelled again as writing to/as a producer, so that it can publish an extend a real world use case like sending emails/SMS/Notif of confirmation etc
- The Layout of the theatre is configurable via a yaml file (sort of another datastore) with custom seats in each row (which can with few efforts can support realworld usecase) => Extensible  
