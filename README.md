Have you ever wanted to turn **coding mistakes into measurable feedback? Impact Counter** is a Python utility for [Jupyter]([url](https://jupyter-notebook.readthedocs.io/)) and [Google Colab]([url](https://colab.research.google.com/)) that logs notebook errors, and counts failures - letting you use tracked errors for impact play as **reinforcement learning to improve your coding over time**.

Perfect for:
- Turn notebook crashes into actionable insights
- **Gamify debugging with error accountability**
- Measure coding progress over time
- Learn Python by reinforcing better coding habits

### Features:
- 🔥 Real-time counter — see how many times your code failed
- 📝 Error logging — keeps track of what failed, when, and in which function
- ☁️ Backend support — store logs locally (SQLite) which you can append to your backend database. *I use Airtable, I've added a helper class to interact with it but this is optional*

## Repository Structure
This repo contains the Python package (notebook_error_logger), a sample notebook, and scripts for logging errors and syncing them with Airtable or SQLite.

## License
`notebook_error_logger` is licensed under the MIT License. See the LICENSE.md file for more details.
