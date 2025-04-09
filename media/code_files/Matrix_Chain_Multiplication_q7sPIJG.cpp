#include <bits/stdc++.h>

using namespace std;

void printOptimalParens(const vector<vector<int>> &solution, int i, int j)
{
    if (i == j)
    {
        cout << "A" << i;
    }
    else
    {
        cout << "(";
        printOptimalParens(solution, i, solution[i][j]);
        printOptimalParens(solution, solution[i][j] + 1, j);
        cout << ")";
    }
}

int MCM_TopDown(const vector<int> &dimensions, int i, int j, vector<vector<int>> &dp, vector<vector<int>> &solution)
{
    if (i == j)
    {
        return 0;
    }

    if (dp[i][j] != -1)
    {
        return dp[i][j];
    }

    dp[i][j] = INT_MAX;

    for (int k = i; k < j; k++)
    {
        int cost = MCM_TopDown(dimensions, i, k, dp, solution) + MCM_TopDown(dimensions, k + 1, j, dp, solution) + dimensions[i - 1] * dimensions[k] * dimensions[j];
        if (cost < dp[i][j])
        {
            dp[i][j] = cost;
            solution[i][j] = k;
        }
    }

    return dp[i][j];
}

void MCM_TopDown(const vector<int> &dimensions)
{
    int n = dimensions.size() - 1;
    vector<vector<int>> dp(n + 1, vector<int>(n + 1, -1));
    vector<vector<int>> solution(n + 1, vector<int>(n + 1, 0));

    int minCost = MCM_TopDown(dimensions, 1, n, dp, solution);

    cout << "Cost of Matrix Chain Multiplication is : " << minCost << endl;
    printOptimalParens(solution, 1, n);
}

void MCM(const vector<int> &dimensions)
{
    int n = dimensions.size() - 1;

    vector<vector<int>> costMatrix(n + 1, vector<int>(n + 1, 0));
    vector<vector<int>> solution(n, vector<int>(n + 1, 0));

    for (int i = 1; i <= n; i++)
    {
        costMatrix[i][i] = 0;
    }

    for (int l = 2; l <= n; l++)
    {
        for (int i = 1; i <= (n - l + 1); i++)
        {
            int j = i + l - 1;
            costMatrix[i][j] = INT_MAX;
            for (int k = i; k < j; k++)
            {
                int minCost = costMatrix[i][k] + costMatrix[k + 1][j] + (dimensions[i - 1] * dimensions[k] * dimensions[j]);
                if (minCost < costMatrix[i][j])
                {
                    costMatrix[i][j] = minCost;
                    solution[i][j] = k;
                }
            }
        }
    }

    for (int i = 1; i <= n; i++)
    {
        for (int j = 1; j <= n; j++)
        {
            if (i <= j)
            {
                cout << costMatrix[i][j] << " ";
            }
            else
            {
                cout << "   ";
            }
        }
        cout << endl;
    }

    cout << "Cost of Matrix Chain Multiplication is : " << costMatrix[1][n] << endl;
    printOptimalParens(solution, 1, n);
}

int main()
{
    int n;
    cout << "Enter the number of matrices (n) : " << endl;
    cin >> n;

    cout << "You have to provide n + 1 dimensions : " << endl;

    vector<int> dimensions(n + 1, 0);

    int temp;
    for (int i = 0; i <= n; i++)
    {
        cin >> temp;
        dimensions[i] = temp;
    }

    MCM(dimensions);

    MCM_TopDown(dimensions);
    return 0;
}

// #include <bits/stdc++.h>

// using namespace std;

// int minDistance(string word1, string word2)
// {
//     int m = word1.size();
//     int n = word2.size();
//     vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));

//     for (int i = 0; i <= m; ++i)
//     {
//         for (int j = 0; j <= n; ++j)
//         {
//             if (i == 0)
//             {
//                 dp[i][j] = j;
//             }
//             else if (j == 0)
//             {
//                 dp[i][j] = i;
//             }
//             else if (word1[i - 1] == word2[j - 1])
//             {
//                 dp[i][j] = dp[i - 1][j - 1];
//             }
//             else
//             {
//                 dp[i][j] = 1 + min({dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]});
//             }
//         }
//     }
//     return dp[m][n];
// }

// int main()
// {
//     string word1 = "horse";
//     string word2 = "ros";
//     cout << "The minimum edit distance is: " << minDistance(word1, word2) << endl;
//     return 0;
// }