Feature: Cards
  Testing Trello API as Sandbox Tests

  Scenario: View All Cards in A Board
	Given I have an existing board
	When I view all available cards
	Then I can view all my cards


  Scenario: Create A Card
    Given I have an existing board
	And I have an existing list
	When I add a card with the following items to the top of list
	Then my card is added successfully
	When I add a card with the following items to the bottom of list
	Then my card is added successfully