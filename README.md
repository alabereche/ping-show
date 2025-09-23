# CS2 Ping Monitor

A lightweight desktop application that monitors ping to Counter-Strike 2 servers across Europe in real-time.

## Screenshot

![CS2 Ping Monitor](screenshot.png)

*Real-time ping monitoring with dark theme and server status indicators*

## What This Application Does

This application continuously monitors your internet connection to Counter-Strike 2 servers across Europe. It shows you the ping (latency) to each server in real-time, helping you choose the best server for gaming.

**Ping** = The time it takes for data to travel from your computer to the server and back. Lower ping = better gaming experience.

## Installation & Setup

### For End Users (No Installation Required)

1. **Download** the entire project folder
2. **Extract** all files to a folder on your computer
3. **Run** the application using one of these methods:


### For Developers

1. **Install Python 3.6+** on your system
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run source code**: `python floating_ping_monitor.py`
4. **Build executable**: `pyinstaller cs2_monitor_final.spec`

## How to Use

1. **Launch** the application using any method above
2. **Wait** 2-3 seconds for initial ping results
3. **Monitor** the ping values updating every second
4. **Choose** servers with green or orange ping for gaming
5. **Drag** the window by clicking anywhere and moving your mouse
6. **Exit** by pressing ESC or right-clicking and selecting "Exit"

## Understanding the Results

- 🟢 **Green (<100ms)** - Excellent ping, perfect for gaming
- 🟠 **Orange (>100ms)** - Good ping, acceptable for gaming
- 🔴 **Red (ERROR)** - Server unreachable (may still work in-game)

## Controls

- **Click anywhere** - Drag window to move it
- **F5** - Refresh ping data
- **Space** - Toggle always on top mode
- **ESC** - Exit application
- **Right-click** - Open context menu

## Features

- **Real-time monitoring** - Updates every 1 second
- **Official CS2 servers** - France, Germany, UK, Spain, Sweden, Austria, Belgium
- **Dark theme** - Easy on the eyes
- **Floating window** - Always stays on top of other windows
- **Draggable** - Click anywhere to move
- **Silent operation** - No console windows or popups

## Important Notes

- **CS2 servers often show "ERROR"** because they block ping requests for security. This is normal behavior.
- **Use the CS2 game client** to test actual connectivity to servers
- **Lower ping = better gaming experience** - choose servers with green or orange ping
- **The application runs continuously** until you close it

## System Requirements

- **Windows 10/11** (64-bit)
- **No additional software required** - runs standalone
- **Internet connection** for ping testing

## Troubleshooting

- **Application won't start**: Try running as administrator
- **No ping results**: Check your internet connection
- **All servers show ERROR**: This is normal for CS2 servers
- **Window won't move**: Click and drag from any part of the window

## Gallery

### Main Interface
![Main Interface](screenshot.png)

### Features Overview
- **Real-time Updates**: Ping values refresh every second
- **Server Categories**: Organized by region (Europe, MENA, Gaming)
- **Color-coded Status**: Green (excellent), Orange (good), Red (error)
- **Floating Window**: Always stays on top for easy monitoring
