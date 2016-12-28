Feature: User Signup
  As an anonymous user
  I want to be able to register
  So I can access my personal data

  Scenario: Register new user
    Given I have the following unregistered user with given information:
    | username      | password1  | password2  | email                   |
    | ratuljain1991 | scooty2310 | scooty2310 | ratuljain1991@gmail.com |
    When I send a POST request to "/rest-auth/registration/"
    Then I get a 201 response


