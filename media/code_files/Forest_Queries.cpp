#include <bits/stdc++.h>

using namespace std;

typedef long long ll;

void solve()
{
    ll n, q;
    cin >> n >> q;
    vector<vector<ll>> v(n, vector<ll>(n));
    char c;
    for (ll i = 0; i < n; i++)
    {
        for (ll j = 0; j < n; j++)
        {
            cin >> c;
            if (c == '.')
                v[i][j] = 0;
            else if (c == '*')
                v[i][j] = 1;
        }
    }
    vector<vector<ll>> pre(n, vector<ll>(n, 0));
    for (ll i = 0; i < n; i++)
    {
        for (ll j = 0; j < n; j++)
        {
            pre[i][j] += v[i][j];
            if (j >= 1)
            {
                pre[i][j] += pre[i][j - 1];
            }
            if (i >= 1)
            {
                pre[i][j] += pre[i - 1][j];
            }
            if (i >= 1 && j >= 1)
            {
                pre[i][j] -= pre[i - 1][j - 1];
            }
        }
    }
    while (q--)
    {
        ll i1, j1, i2, j2;
        cin >> i1 >> j1 >> i2 >> j2;
        i1--;
        j1--;
        i2--;
        j2--;
        ll ans = 0;
        ans += pre[i2][j2];
        if (j1 >= 1)
        {
            ans -= pre[i2][j1 - 1];
        }
        if (i1 >= 1)
        {
            ans -= pre[i1 - 1][j2];
        }
        if (i1 >= 1 && j1 >= 1)
        {
            ans += pre[i1 - 1][j1 - 1];
        }
        cout << ans << endl;
    }
}
int main()
{
    /*Darshan Kania*/
    solve();
    return 0;
}