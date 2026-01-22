import java.util.*;
import java.io.*;
/*
    NAME: Katrina Dotzlaw
    COURSE: Comp 2140 A02 INSTRUCTOR: Robert Guderian
    ASSIGNMENT 3
    PURPOSE: to implement a game of War using stacks and queues

    ORDER OF SUITS: 0 = Spades, 1 = Clubs, 2 = Diamonds, 3 = Hearts
        In the Deck -- Spades: 0-12, Clubs: 13-25, Diamonds: 26-38, Hearts: 39-51
 */

public class A3DotzlawKatrina {
    public static void main (String args[]){
        //Create a new war Game and begin the game
        WarGame w = new WarGame();
        w.playGame();
    }
    //Final Variables
    public static final int MAX_SIZE = 53;//because we want to use n-1 available space (cards are 0-51 space 52 is always free)
    //Class - Queue: used to implement the players hand
    public static class Queue{
        int[] player;
        int start;
        int end;
        public  Queue(){
            player = new int[MAX_SIZE];//queue must be size of deck, as a player wins when they have all 52 cards
            Arrays.fill(player, -1); //set all values in player[] to -1, for testing convenience
            start = 0; //start and end start at 0 because there is nothing in the array
            end = 0;
        }
        //Enter - add to the end of the array: indecies 0-51 are in use with index 52 not in uses
        public void enter(int item){
            //end++;
            if(end!=player.length-1 && item!=-1) {//make sure there is room to add to array
                try {
                    player[end] = item;
                    end++;//increment end pointer
                }catch(Exception e){}
            }
        }
        //Leave - from the front of the queue
        public int leave(){
            int item;
            item = player[start];//always removes from the start of queue
            for(int i = 1; i < MAX_SIZE-1; i++)//loop required to move all elements left one space
                player[i-1] = player[i];
           end--;//decrement end pointer
            return item;
        }
    }//end of queue class
    //implement players revealed cards - stacks - array implementation
    public static class Stack{
        int[] revealedCards; //holds all the players revealed cards
        int top;//keeps track of the top of the array
        public Stack(){
            revealedCards = new int[MAX_SIZE];
            Arrays.fill(revealedCards, -1); //set all values in revealedCards[] to -1 - for testing convenience
            top = 0;//keeps track of the index of the top item in stack
        }
        //Push - add to top of stack
        public void push(int item){
            if(item!=-1) {//only add the item if it is NOT -1 (not a marker for an empty space)
                revealedCards[top] = item;
                top++;//increment pointer
          }
        }
        //Pop - remove from the top of the stack
        public int pop(){
            int item = -1;
            if(top>0) {//make sure there is something in the stack to remove
                //System.out.println("Top of Stack is: "+top);
            item = revealedCards[top];
            revealedCards[top] = -1;//this indicates that the spot is now empty
                top--;
                //revealedCards[top] = -1;//erase the item that was here
            }
            else {//can't decrement top pointer because it is already pointing to spot 0
                item = revealedCards[0];
                 revealedCards[0] = -1;//this indicates that the spot is now empty
            }
            return item;
        }
        //Peek - look at top item of stack
        public int peek(){
            int iPeek = -1;
            if(top!=0)
                iPeek = revealedCards[top-1];
            return iPeek;
        }

    }
    //setup game - deal 1/2 cards to each player (add them to the queues)
    public static class WarGame{
        //Declare Booleans
        boolean player1Won = false; //becomes true if game is done and player1 still has cards
        boolean player2Won = false; //becomes true if game is done and player2 still has cards
        boolean warEndedGame = false;
        //Declare stack and queue variables
        Queue player1;
        Queue player2;
        Stack p1Revealed;
        Stack p2Revealed;
        public WarGame(){//Constructor to implement stacks and queues
            //make 2 new queues
            player1 = new Queue();
            player2 = new Queue();
            //Make 2 Stacks that contain the revealed cards of each player
            p1Revealed = new Stack();
            p2Revealed = new Stack();
            //Make a new Deck
            int [] deck = makeDeck();
            //deal 1/2 the deck to each of the players queues
            print(deck);
            deal(player1, player2, deck);
            print(player1);
            print(player2);

        }
        //Helper Function for dealing Cards - after the deck is shuffled, split the deck and give half to each player (this is essentially the same as dealing)
        public void deal(Queue p1, Queue p2, int[] deck){
            int half = deck.length/2;
            //deal first half of deck to player 1
            for(int i = 0; i < half; i++)
                p1.enter(deck[i]);
            //deal second half of deck to player 2
            for(int i = half; i < deck.length;i++)
                p2.enter(deck[i]);
        }
        //setup deck
        public int[] makeDeck(){
            //the values in deck are the 'c' values that are used to calculate the rank and suit
            int [] deck = new int[MAX_SIZE-1];
            for(int i = 0; i < MAX_SIZE-1; i++)
                deck[i] = i;//put 0 - 51 in the deck
            //perform a set number of random swaps - doing this ensures that the numbers are only in the deck once
            for(int s = 0; s < 5000; s++){//swaps cards 50000 times randomly
                int tempIndex1 = (int)(Math.random()*51);
                int tempIndex2 = (int)(Math.random()*51);
                int temp = deck[tempIndex1];
                deck[tempIndex1] = deck[tempIndex2];
                deck[tempIndex2] = temp;
            }
            return deck;//returns a deck that has been shuffled
        }
        //Helper method for calculating the rank - takes an integer 'c' and calculates rank using given formula
        public int getRank(int c){
           return (1+(c%13));//[1-13]
        }
        //Private helper method that contains a string array that maps to all possible cards and returns the string that correlates to the parameter c
       private String intToString(int c){
            //String sReturn = "";
           String [] sMap = {"A","2","3","4","5","6","7","8","9","10","J","Q","K",""};
           //System.out.println(sMap.length);
          return sMap[c-1];
        }

        //Helper method for calculating the suit - takes an integer 'c' and calculates suit using the given formula
        public char getSuit(int c) {//suits dont matter for comparisons - does matter for printing out gameplay
            int iSuit = (int)(c/13); //0,1,2,3
            char cSuit = ' ';
            if(iSuit==0)
                cSuit = 'S';//suit is spade
            else if(iSuit==1)
                cSuit = 'C';//suit is clubs
            else if(iSuit==2)
                cSuit = 'D';//suit is diamond
            else
                cSuit = 'H';//suit is hearts
            //System.out.println("Suit is: "+cSuit);
            return cSuit;
        }//end of getSuit
        //method that controls a round
        public void runRound(){
            //player flips over front card and compares to other player
            p1Revealed.push(player1.leave());//add to p1 stack
            p2Revealed.push(player2.leave());//add to p2 stack
            //store the top item in a variable - easier to enter queue if its stored in a variable
            int p1Card = p1Revealed.peek();
            int p2Card = p2Revealed.peek();
            //store rank
            int p1Rank = getRank(p1Revealed.peek());//gets the rank of the card
            int p2Rank = getRank(p2Revealed.peek());//gets rank of card
            //store suit
            char p1Suit = getSuit(p1Revealed.peek());
            char p2Suit =  getSuit(p2Revealed.peek());
            //System.out.println("Player 1 Suit: "+p1Suit);
            //Compare cards
            //if the 2 cards do NOT have equal rank, the player with the highest rank (A-K) wins
            if(p1Rank!=p2Rank){
                    System.out.println("Player 1 has: " + intToString(p1Rank) + " of " + p1Suit + ", Player 2 has: " + intToString(p2Rank) + " of " + p2Suit);
                if(p1Rank > p2Rank){//player1 wins all cards
                    System.out.println("Player 1 Wins Round");
                    //add all cards to player1's queue
                  player1.enter(p1Card);
                  player1.enter(p2Card);
                    //remove from player stack
                    p1Revealed.pop();
                    p2Revealed.pop();
                }
                else{//player2 wins all cards
                    System.out.println("Player 2 Wins Round");
                    //add all cards to player2's queue
                    player2.enter(p1Card);
                    player2.enter(p2Card);
                    //remove from player stack
                    p1Revealed.pop();
                    p2Revealed.pop();
                }
            }//there is no war
            //if the 2 cards ARE equal rank, then its WAR
            else{
                System.out.println("Player 1 has: " + intToString(p1Rank) + " of " + p1Suit + ", Player 2 has: " +intToString(p2Rank) + " of " + p2Suit);
                System.out.println("Players are at WAR!");
                war();
            }//there is a war
           /*System.out.print("Player 1 Stack: ");
            print(p1Revealed);
            System.out.print("Player 2 Stack: ");
            print(p2Revealed);
            System.out.print("Player 1 Queue: ");
            print(player1);
            System.out.print("Player 2 Queue:  ");
            print(player2);
            */
        }//end of runRound
        //method that controls a war (called in runRound()) and runRound() is called in this function
        public void war(){
            //isWar = true;//players are at war
            if(!warEndedGame) {
                //Each player reveals 2 more cards in a stack on top of the already revealed card
                //Player1
                p1Revealed.push(player1.leave());
                System.out.print("Player 1 Ante: " + intToString(getRank(p1Revealed.peek())) + " of " + getSuit(p1Revealed.peek()));
                p1Revealed.push(player1.leave());
                System.out.println(" and " + intToString(getRank(p1Revealed.peek())) + " of " + getSuit(p1Revealed.peek()));
                //Player 2
                p2Revealed.push(player2.leave());
                System.out.print("Player 2 Ante: " + intToString(getRank(p2Revealed.peek())) + " of " + getSuit(p2Revealed.peek()));
                p2Revealed.push(player2.leave());
                System.out.println(" and " + intToString(getRank(p2Revealed.peek())) + " of " + getSuit(p2Revealed.peek()));
                //Then, players reveal the last card which goes on top of the stack.
                //Player 1 Last Card
                p1Revealed.push(player1.leave());
                System.out.println("Player 1 has " + intToString(getRank(p1Revealed.peek())) + " of " + getSuit(p1Revealed.peek()));
                //Player 2 Last Card
                p2Revealed.push(player2.leave());
                System.out.println("Player 2 has " + intToString(getRank(p2Revealed.peek())) + " of " + getSuit(p2Revealed.peek()));
                //Compare last cards added
                int p1Rank = getRank(p1Revealed.peek());
                //int p1Suit = getSuit(p1Revealed.peek());
                int p2Rank = getRank(p2Revealed.peek());
               // int p2Suit = getSuit(p2Revealed.peek());
                if(p1Rank!=p2Rank){//there is no war
                    if(p1Rank>p2Rank){
                        //p1 wins all cards
                       int size = p1Revealed.top;
                       for(int i = 0; i <= size; i++){
                           player1.enter(p1Revealed.pop());
                           player1.enter(p2Revealed.pop());
                       }//loop
                        System.out.println("Player 1 Wins the War!");
                    }//p1 wins
                    else if(p2Rank>p1Rank){
                        //p2 wins ALL cards - antes and compared
                        int size = p2Revealed.top;
                        for(int i = 0; i <= size; i++){
                            player2.enter(p2Revealed.pop());
                            player2.enter(p1Revealed.pop());
                        }//loop
                        System.out.println("Player 2 Wins the War!");
                    }//p2 wins
                    else{//someone is out of cards
                        if(!checkCards(player1)){
                            warEndedGame = true;
                        }
                        if(!checkCards(player2))
                            warEndedGame = true;
                    }
                }//there is no war
                else{//there is another war
                    war();//make sure its not infinite recursion
                }
            }//if both players still have cards
            /*else{
                //System.out.println("Someone ran out of cards!");
                isDone();//game is over.
            }//if someone has run out of cards*/
        }//end of war()
        //Private method called in war() that checks if there are not enough cards to complete the war
        private boolean checkCards(Queue q){
            boolean bReturn = true;//assume there are enough cards to finish war
            int i = 0;
            int count  = 0;
            while(q.player[i]!=-1){
                count++;
            }
            if(count<=3)
                bReturn = false;
            return bReturn;
        }//end of check cards
        //Private method that checks if the  given queue is empty
        public boolean isQEmpty(Queue q){
            boolean bEmpty = true;//assume queue is empty.
            for(int i = 0; i < q.player.length;i++){
                if(q.player[i]!=-1)
                    bEmpty = false;
            }
            return bEmpty;
        }//end of isQEmpty
        //method that detects whether the game is won or not
        public boolean isDone(){
            //Game is done when a player runs out of cards. Player with cards left over wins
            boolean won = false;
            if(isQEmpty(player1)){//then the queue is empty
                won = true;
                player2Won = true;//player1 has won the game
                System.out.println("Player 2 has won the game!");
            }
            if(isQEmpty(player2)){//then the queue is empty
                won = true;
                player1Won = true; //player2 has won the game
                System.out.println("Player 1 has won the game!");
            }
            return won;
        }//end of isDone
        //method to run game (playGame)
        public void playGame(){
            //call runRound until someone has won
            System.out.println("Game Begins!");
            while(!isDone()){
                runRound();
            }
            System.out.println("Game is over");
        }//end of playGame
        /*
            Below are 3 print methods that were used to test that the implemtation of stacks and queues work
            Also used to print out the stacks and queues after every round that is run
         */
        //printer method for queues
        public void print(Queue q){
            System.out.println("Queue: ");
            for(int i = 0; i < q.player.length; i++){
               if(q.player[i]!=-1)
                    System.out.print(q.player[i]+", ");
            }
            System.out.println();
        }
        //Printer method for stacks
        public void print(Stack s){
            System.out.println("Stack: ");
            for(int i = 0; i < s.revealedCards.length; i++) {
                if (s.revealedCards[i] != -1)
                    System.out.print(s.revealedCards[i] + ", ");
            }
            System.out.println();
        }
        //Printer method for arrays
        public void print(int[]a){
            System.out.println("Array: ");
            for(int i = 0; i < a.length; i++)
                System.out.print(a[i]+", ");
            System.out.println();
        }
    }//end of WarGame class

} //end of A3DotzlawKatrina
