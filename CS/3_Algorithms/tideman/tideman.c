#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);
void merge_sort(int l, int r);
void merge(int l, int m, int r);
int pair_strength(pair p);
int find_source(void);
bool find_ancester(int tail, int target);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (!strcmp(name, candidates[i]))
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count - 1; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]] += 1;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int i = 0; i < candidate_count - 1; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            if (i == j)
            {
                continue;
            }
            
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count += 1;
            }
            else if (preferences[i][j] < preferences[j][i])
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
                pair_count += 1;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    merge_sort(0, pair_count - 1);
    return;
}

void merge_sort(int l, int r)
{
    if (l >= r)
    {
        return;
    }
    
    int m = (l + r) / 2;
    
    merge_sort(l, m);
    merge_sort(m + 1, r);
    
    merge(l, m, r);
}

void merge(int l, int m, int r)
{
    int lenl = m - l + 1;
    int lenr = r - m;
    
    pair left[lenl];
    pair right[lenr];
    
    for (int i = 0; i < lenl; i++)
    {
        left[i] = pairs[i + l];
    }
    for (int j = 0; j < lenr; j++)
    {
        right[j] = pairs[j + m + 1];
    }
    
    int i = 0;
    int j = 0;
    int k = l;
    while (i < lenl && j < lenr)
    {
        if (pair_strength(left[i]) > pair_strength(right[j]))
        {
            pairs[k] = left[i];
            i += 1;
        }
        else
        {
            pairs[k] = right[j];
            j += 1;
        }
        k += 1;
    }
    
    while (i < lenl)
    {
        pairs[k] = left[i];
        k += 1;
        i += 1;
    }
    
    while (j < lenr)
    {
        pairs[k] = right[j];
        k += 1;
        j += 1;
    }
}

int pair_strength(pair p)
{
    return preferences[p.winner][p.loser];
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        int winner = pairs[i].winner;
        int loser = pairs[i].loser;
        
        if (i != 0)
        {   
            int tail = winner;
            
            if (find_ancester(tail, loser))
            {
                continue;
            }
        }
        
        locked[winner][loser] = true;
    }
    
}

bool find_ancester(int tail, int target)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (locked[i][tail])
        {
            if (i == target)
            {
                return true;
            }
            
            if (find_ancester(i, target))
            {
                return true;
            }
        }
    }
    return false;
}


int find_source(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        bool all_false = true;
        
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[j][i])
            {
                all_false = false;
                break;
            }
        }
        
        if (all_false)
        {
            return i;
        }
        
    }
    return - 1;
}

// Print the winner of the election
void print_winner(void)
{
    int winner = find_source();
    
    printf("%s\n", candidates[winner]);
    return;
}

