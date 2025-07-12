# Fitness Frontend

## Project Overview
Fitness Frontend is a web application designed to help users track their fitness journey. It provides tools for recording workouts, managing routines, analyzing progress, and more. The application is structured to offer a seamless user experience for fitness enthusiasts.

## Features
- **Workout Recorder**: Log cardio and strength workouts.
- **Routine Manager**: Create and manage fitness routines.
- **Analytics**: View historic workout data and post-workout summaries.
- **User Profile**: Manage personal information and preferences.

## Folder Structure
The project is organized as follows:

```
config/         # Configuration files (e.g., URLs)
database/       # CRUD operations for database management
helpers/        # Utility functions (e.g., cache management, UI helpers)
models/         # Data models for exercises, routines, sessions, users, and workouts
pages/          # Web pages grouped by functionality
  analytics/    # Pages for viewing analytics
  recorder/     # Pages for recording workouts
  routine/      # Pages for managing routines
  user/         # Pages for user profile management
app.py          # Main application entry point
home.py         # Home page logic
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/the-tunnster/fitness-frontend.git
   ```
2. Navigate to the project directory:
   ```bash
   cd fitness-frontend
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up configuration files:
   - Create a `.streamlit` folder and add a `config.toml` and `secrets.toml` file.
   - The config file allows you to modify app behaviour from a UI perspective.
   - The secrets file is required if you're using OIDC login. The app will crash without these details.


## Usage
1. Run the application:
   ```bash
   streamlit run app.py
   ```
2. Open your browser and navigate to `http://localhost:8501`.
3. Explore the features of the application.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the Creative Commons Attribution-NonCommercial (CC BY-NC) License. See the LICENSE file for details.

---

Feel free to reach out for any questions or feedback!
