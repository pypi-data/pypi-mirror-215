"""
anonpi: Python Module for Calling Systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The "anonpi" module is a powerful Python package that provides a convenient interface for interacting with calling systems. It simplifies the development of applications that require functionalities such as machine detection, IVR (Interactive Voice Response), DTMF (Dual-Tone Multi-Frequency) handling, recording, playback, and more.

Key Features:
- Machine Detection: Easily detect whether a call is being answered by a human or an automated system, enabling intelligent call handling and routing.
- IVR Support: Build interactive voice response systems by creating menus, prompts, and collecting user input through voice or DTMF tones.
- DTMF Handling: Efficiently capture and process DTMF tones (telephone keypad input) during calls for user interaction, menu navigation, and decision-making.
- Call Recording: Seamlessly record incoming or outgoing calls, enabling compliance with legal requirements, quality monitoring, and archiving for later analysis.
- Playback Functionality: Retrieve and play back pre-recorded audio files during calls, enhancing the user experience and providing personalized content.
- Call Control: Take control of call initiation, termination, and manipulation, allowing for call transfers, forwarding, muting, and more.

Usage:
The "anonpi" module provides a clean and intuitive API, making it easy to integrate calling functionalities into your Python applications. Refer to the documentation for detailed usage instructions, API reference, and examples.

Installation:
You can install the "anonpi" module using pip:
pip install anonpi

Contributing:
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request in the GitHub repository.

License:
This project is licensed under the MIT License.
"""


from call import jsonify, request, Flask , request_finished

__all__ = ['Flask', 
           'request', 
           'jsonify' , 
           'request_finished']