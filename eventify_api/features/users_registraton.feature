Feature: User Signup
  As an anonymous user
  I want to be able to register
  So I can access my personal data

  Scenario: Register new user
    Given I have the following unregistered user with given information:
      | username      | password1    | password2    | email                   |
      | ratuljain1991 | samepassword | samepassword | ratuljain1991@gmail.com |
    When I send a POST request to "/rest-auth/registration/"
    Then I get a 201 response

  Scenario: Register new user with invalid email
    Given I have the following unregistered user with given information:
      | username      | password1    | password2    | email                  |
      | ratuljain1991 | samepassword | samepassword | ratuljain1991gmail.com |
    When I send a POST request to "/rest-auth/registration/"
    Then I get a 400 response
    And the response should be JSON "{"email":["Enter a valid email address."]}":

  Scenario: Register new user with no email
    Given I have the following unregistered user with given information:
      | username      | password1    | password2    | email |
      | ratuljain1991 | samepassword | samepassword |       |
    When I send a POST request to "/rest-auth/registration/"
    Then I get a 400 response
    And the response should be JSON "{ "email": ["This field may not be blank." ]}":

  Scenario: Register new user with username less than 5 characters
    Given I have the following unregistered user with given information:
      | username | password1    | password2    | email                   |
      | four     | samepassword | samepassword | ratuljain1991@gmail.com |
    When I send a POST request to "/rest-auth/registration/"
    Then I get a 400 response
    And the response should be JSON "{"username": ["Ensure this field has at least 5 characters."]}":


  Scenario: Register new user with username more than 15 characters
    Given I have the following unregistered user with given information:
      | username          | password1    | password2    | email                   |
      | fifteencharacters | samepassword | samepassword | ratuljain1991@gmail.com |
    When I send a POST request to "/rest-auth/registration/"
    Then I get a 400 response
    And the response should be JSON "{"username":["Ensure this field has no more than 15 characters."]}":


  Scenario: Register new user when different password is entered in the password 2 field
    Given I have the following unregistered user with given information:
      | username      | password1    | password2         | email                   |
      | ratuljain1991 | samepassword | differentpassword | ratuljain1991@gmail.com |
    When I send a POST request to "/rest-auth/registration/"
    Then I get a 400 response
    And the response should be JSON "{"non_field_errors":["The two password fields didn't match."]}":


  Scenario: Register new user when password1 field is empty
    Given I have the following unregistered user with given information:
      | username      | password1 | password2    | email                   |
      | ratuljain1991 |           | samepassword | ratuljain1991@gmail.com |
    When I send a POST request to "/rest-auth/registration/"
    Then I get a 400 response
    And the response should be JSON "{"password1":["This field may not be blank."]}":

  Scenario: Register new user when password2 field is empty
    Given I have the following unregistered user with given information:
      | username      | password1    | password2 | email                   |
      | ratuljain1991 | samepassword |           | ratuljain1991@gmail.com |
    When I send a POST request to "/rest-auth/registration/"
    Then I get a 400 response
    And the response should be JSON "{"password2":["This field may not be blank."]}":

  Scenario: Register new user when password is less than 8 characters short
    Given I have the following unregistered user with given information:
      | username      | password1 | password2 | email                   |
      | ratuljain1991 | eight     | eight     | ratuljain1991@gmail.com |
    When I send a POST request to "/rest-auth/registration/"
    Then I get a 400 response
    And the response should be JSON "{"password1":["This password is too short. It must contain at least 8 characters."]}":
