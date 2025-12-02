import plotly.graph_objects as go

def demand_closed_form(n, D0=5):
    alpha = 2   
    beta = -1   
    return alpha * (2 ** n) + beta

def simulate_inventory(N, D0=5, I0=50):
    D = [D0]
    I = [I0]
    for n in range(1, N + 1):
        Dn = 2 * D[n-1] + 3
        D.append(Dn)
        In = I[n-1] - Dn + D[n-1]
        I.append(In)
    return D, I

def plot_demand_inventory(D, I):
    n = list(range(len(D)))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n, y=D, mode='lines+markers', name='Demand'))
    fig.add_trace(go.Scatter(x=n, y=I, mode='lines+markers', name='Inventory'))
    fig.update_layout(title='Weekly Demand and Inventory',
                      xaxis_title='Week n',
                      yaxis_title='Units')
    fig.show()

def simulate_branching(N, p0=0.4, p1=0.4, p2=0.2, trials=1000):
    import random
    paths = []
    means = [0] * (N + 1)
    for _ in range(trials):
        z = 1
        path = [z]
        for _ in range(N):
            # sample offspring for each infected
            new_z = 0
            for _ in range(z):
                r = random.random()
                if r < p0:
                    off = 0
                elif r < p0 + p1:
                    off = 1
                else:
                    off = 2
                new_z += off
            z = new_z
            path.append(z)
        paths.append(path)
    for gen in range(N + 1):
        means[gen] = sum(path[gen] for path in paths) / trials
    return means

def plot_epidemic(means, R0):
    n = list(range(len(means)))
    theoretical = [R0 ** k for k in n]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=n, y=means, mode='lines+markers',
                             name='Simulated mean infections'))
    fig.add_trace(go.Scatter(x=n, y=theoretical, mode='lines',
                             name='Theoretical R0^n'))
    fig.update_layout(title='Branching Process Epidemic (Mean Infections)',
                      xaxis_title='Generation n',
                      yaxis_title='Number of infections')
    fig.show()

def main():
    while True:
        print("Choose scenario:")
        print("1) Inventory & demand")
        print("2) Epidemic branching process")
        print("0) Exit")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            N = int(input("Simulate up to week N = "))
            D, I = simulate_inventory(N)
            plot_demand_inventory(D, I)
        elif choice == '2':
            N = int(input("Simulate up to generation N = "))
            p0, p1, p2 = 0.4, 0.4, 0.2  # you can also prompt user
            R0 = p1 + 2 * p2
            means = simulate_branching(N, p0, p1, p2)
            plot_epidemic(means, R0)
        elif choice == '0':
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
