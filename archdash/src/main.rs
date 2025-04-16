// main.rs
use anyhow::Result;
use crossterm::event::{self, Event, KeyCode};
use ratatui::prelude::*;
use std::time::{Duration, Instant};

mod app;
mod ui;
mod system;

fn main() -> Result<()> {
    // Initialize terminal
    let mut terminal = initialize_terminal()?;
    
    // Create app state
    let mut app = app::App::new();
    
    // Main event loop
    let tick_rate = Duration::from_millis(250);
    let mut last_tick = Instant::now();
    
    loop {
        // Draw UI
        terminal.draw(|frame| ui::draw(frame, &app))?;
        
        // Handle input
        let timeout = tick_rate
            .checked_sub(last_tick.elapsed())
            .unwrap_or_else(|| Duration::from_secs(0));
            
        if event::poll(timeout)? {
            if let Event::Key(key) = event::read()? {
                if key.code == KeyCode::Char('q') {
                    break;
                }
                app.handle_input(key);
            }
        }
        
        // Update state
        if last_tick.elapsed() >= tick_rate {
            app.update()?;
            last_tick = Instant::now();
        }
    }
    
    // Cleanup
    restore_terminal()?;
    Ok(())
}