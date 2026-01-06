# Data Visualization with Python using Matplotlib, Seaborn, Plotly and Streamlit

> Note Direct access to the course: [cours](src/cours.html)

This quick course introduces fundamentals of Data Vizualization with Python.
Its basics components are:
- Matplotlib: provides the tools to make any (static) chart, on which the following are based
- Seaborn: based on Matplotlib, provides shortcuts for attractive charts, along with additional ready to use graphs (e.g. pairplot)
- Plotly: based on Seaborn, provides interactivity with labels and zoom level, along with additional ready to use graphs (e.g. sunburst)
- Streamlit: provides interactivity with the user as in any dashboard (Tableau Software, Power BI)

## Instruction for Streamlit Workshop

The objective of this workshop is to transition from static data analysis to interactive web applications, ensuring reproducibility and ease of sharing within the scientific community.

We will use a cloud-based development environment to avoid local installation issues.

### 1. Project Initialization (Forking)

To modify the source code and save your progress, you must first create a personal copy of this repository on your GitHub account.

1.  Navigate to the top-right corner of this page.
2.  Click on the **Fork** button.
3.  Confirm by clicking **Create fork**.

> **Note:** You now possess a personal copy of the repository (`your-username/repository-name`). All subsequent operations must be performed on this version.


### 2. Environment Setup (GitHub Codespaces)

We will utilize a pre-configured cloud environment (Codespace) that contains all necessary dependencies (Python, Pandas, Plotly, Streamlit).

1.  Click on the green **Code** button.
2.  Select the **Codespaces** tab.
3.  Click on **Create codespace on main**.

A Visual Studio Code interface will open in your browser. Please allow a few minutes for the environment to initialize fully.

### 3. Running the Application

Once the terminal (the command line interface at the bottom of the screen) is ready, execute the following command to start the Streamlit server:

```bash
python -m streamlit run app.py
```

A notification will appear in the bottom-right corner. Click **Open in Browser** to view the dashboard.

*If the notification does not appear, navigate to the **Ports** tab (next to the Terminal tab) and click on the "Globe" icon to access the application.*

### 4. Development and Version Control

You may now modify the `app.py` file to alter the visualization parameters or add new charts. Once your changes are complete, you must push them to your GitHub repository.

Execute the following commands sequentially in the terminal:

1. Stage the changes:
```bash
git add app.py
```

2. Commit the changes with a descriptive message:
```bash
git commit -m "Updated visualization parameters"
```

3. Push the changes to the remote repository:
```bash
git push
```

Or simply ask the AI agent (Claude) to do it for you!

> **Authentication:** If this is your first commit from a Codespace, Git may prompt you to authorize the connection. Please follow the on-screen instructions.

### 5. Deployment (Streamlit Community Cloud)

To make your dashboard accessible to collaborators via a public URL, we will deploy it using Streamlit Community Cloud.

1. Open a new tab and navigate to **[share.streamlit.io](https://share.streamlit.io/)**.
2. Click on **Continue with GitHub**.
3. Simply click **Authorize streamlit** at the bottom of the page.
4. Click on **New app**.
5. Select **Use existing repo**.
6. In the repository dropdown menu, select your forked repository.
7. Click **Deploy!**.

---

This course has been made originally for UPEC (Université Paris Est Créteil) located in France in the Paris area. It is expected to be taught in a 1 day workshop with 3 hours of lectures and 4 hours of exercises.


Coucou (alexis)
