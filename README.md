<div align="center" markdown="1">

<a href="https://gitlab.com/dr.graphdesigner-group/dr.graphdesigner-project">
    <img src=".github/logo.svg" height="80" alt="OrbioCRM Logo">
</a>

<h1>OrbioCRM</h1>

**Simplify Sales, Amplify Relationships**

[![GitLab Release](https://img.shields.io/gitlab/v/release/dr.graphdesigner-group/dr.graphdesigner-project?sort=semver)](https://gitlab.com/dr.graphdesigner-group/dr.graphdesigner-project/-/releases)

<div>
    <picture>
        <source media="(prefers-color-scheme: dark)" srcset=".github/screenshots/FrappeCRMHeroImage.png">
        <img width="1402" alt="OrbioCRM Hero Image" src=".github/screenshots/FrappeCRMHeroImage.png">
    </picture>
</div>

[GitLab](https://gitlab.com/dr.graphdesigner-group/dr.graphdesigner-project) - [Documentation](#)

</div>

## OrbioCRM

OrbioCRM is a simple, affordable, open-source CRM tool designed for modern sales teams with unlimited users. OrbioCRM is crafted for providing a great user experience, packed with features for core CRM activities helping you build strong customer relationships while keeping things clean and organised.

### Motivation

The motivation behind building OrbioCRM stems from the need for a simple, customizable, and open-source solution tailored to modern business needs. Many existing CRMs are either too complex, overly generic, or locked behind steep pricing models that hinder accessibility and flexibility. OrbioCRM was designed to bridge this gap, offering a tool that empowers businesses to manage their customer relationships seamlessly while being easy to adapt to specific workflows. Built on a modern full-stack framework, it prioritizes usability, extensibility, and affordability, making it an ideal choice for growing teams and organizations looking for a CRM that aligns with their unique processes.

### Key Features

-   **User-Friendly and Flexible:** A simple, intuitive interface that’s easy to navigate and highly customizable, enabling teams to adapt it to their specific processes effortlessly.
-   **All-in-One Lead/Deal Page:** Consolidate all essential actions and details—like activities, comments, notes, tasks, and more—into a single page for a seamless workflow experience.
-   **Kanban View:** Manage leads and deals visually with a drag-and-drop Kanban board, offering clarity and efficiency in tracking progress across stages.
-   **Custom Views:** Design personalized views to organize and display leads and deals using custom filters, sorting, and columns, ensuring quick access to the most relevant information.

    <details>
    <summary>Screenshots</summary>

    <div>
        <picture>
            <source media="(prefers-color-scheme: dark)" srcset=".github/screenshots/LeadList.png">
            <img width="1402" alt="Lead List" src=".github/screenshots/LeadList.png">
        </picture>
    </div>
    <div>
        <picture>
            <source media="(prefers-color-scheme: dark)" srcset=".github/screenshots/LeadPage.png">
            <img width="1402" alt="Lead Page" src=".github/screenshots/LeadPage.png">
        </picture>
    </div>
    <div>
        <picture>
            <source media="(prefers-color-scheme: dark)" srcset=".github/screenshots/EmailTemplate.png">
            <img width="1402" alt="Email Template" src=".github/screenshots/EmailTemplate.png">
        </picture>
    </div>
    <div>
        <picture>
            <source media="(prefers-color-scheme: dark)" srcset=".github/screenshots/CallUI.png">
            <img width="1402" alt="Call UI" src=".github/screenshots/CallUI.png">
        </picture>
    </div>
    <div>
        <picture>
            <source media="(prefers-color-scheme: dark)" srcset=".github/screenshots/CallLog.png">
            <img width="1402" alt="Call Log" src=".github/screenshots/CallLog.png">
        </picture>
    </div>

    </details>

### Integrations

-   **Twilio:** Integrate Twilio to make and receive calls from the CRM. You can also record calls. It is a built-in integration.
-   **Exotel:** Integrate Exotel to make and receive calls via agents mobile phone from the CRM. You can also record calls. It is a built-in integration.
-   **WhatsApp:** Integrate WhatsApp to send and receive messages from the CRM.
-   **ERPNext:** Integrate with [ERPNext](https://erpnext.com) to extend the CRM capabilities to include invoicing, accounting, and more.

### Under the Hood

- A full-stack web application framework.
- A Vue-based UI library, to provide a modern user interface.

### Compatibility
This app is compatible with the following versions of Frappe and ERPNext:

| CRM branch            | Stability | Frappe branch        | ERPNext branch       |
| :-------------------- | :-------- | :------------------- | :------------------- |
| main - v1.x           | stable    | v15.x & v16.x        | v15.x & v16.x        |
| develop - future/v2.x | unstable  | develop - future/v17 | develop - future/v17 |

## Getting Started (Production)

### Self Hosting

Deploy OrbioCRM using Docker on your server.

## Getting Started (Development)

### Local Setup

1. Setup the framework bench.
1. In the frappe-bench directory, run `bench start` and keep it running.
1. Open a new terminal session and cd into `frappe-bench` directory and run following commands:
    ```sh
    $ bench get-app crm
    $ bench new-site sitename.localhost --install-app crm
    $ bench browse sitename.localhost --user Administrator
    ```
1. Access the crm page at `sitename.localhost:8000/crm` in your web browser.

**For Frontend Development**
1. Open a new terminal session and cd into `frappe-bench/apps/crm`, and run the following commands:
    ```
    yarn install
    yarn dev
    ```
1. Now, you can access the site on vite dev server at `http://sitename.localhost:8080`

**Note:** You'll find all the code related to OrbioCRM's frontend inside `frappe-bench/apps/crm/frontend`

### Docker

You need Docker, docker-compose and git setup on your machine. Refer [Docker documentation](https://docs.docker.com/). After that, follow below steps:

**Step 1**: Setup folder and download the required files

    mkdir orbiocrm
    cd orbiocrm

    # Download the docker-compose file
    wget -O docker-compose.yml https://gitlab.com/dr.graphdesigner-group/dr.graphdesigner-project/-/raw/main/docker/docker-compose.yml

    # Download the setup script
    wget -O init.sh https://gitlab.com/dr.graphdesigner-group/dr.graphdesigner-project/-/raw/main/docker/init.sh

**Step 2**: Run the container and daemonize it

    docker compose up -d

**Step 3**: The site [http://crm.localhost:8000/crm](http://crm.localhost:8000/crm) should now be available. The default credentials are:

-   Username: Administrator
-   Password: admin

## Learn and connect

-   Documentation: #
