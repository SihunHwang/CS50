#include <stdio.h>
#include <cs50.h>

int main(void)
{   
    //prompt user for their name
    string name = get_string("What is your name?\n");
    //greet user
    printf("hello, %s\n", name);
}