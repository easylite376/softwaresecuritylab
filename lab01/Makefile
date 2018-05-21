test:
	python3 tool.py http://localhost:8080 -i test.txt

start-apache:
	@docker run -d --name apache-test -p 8080:80 easylite376/test-apache

clean:
	@docker rm -f apache-test
