#!/usr/bin/env python3
"""
Command Line Interface for HumAIne-chatbot Testing

This script provides an interactive CLI to test the chatbot's capabilities.
"""

import requests
import json
import time
import sys
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:8000"

class HumAIChatbotCLI:
    """Interactive CLI for testing HumAIne-chatbot"""
    
    def __init__(self):
        self.session_id = None
        self.user_id = None
        self.conversation_active = False
        
    def check_health(self):
        """Check if the chatbot is running"""
        try:
            response = requests.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                health_data = response.json()
                print(f"✅ HumAIne-chatbot is running!")
                print(f"   Status: {health_data['status']}")
                print(f"   Active conversations: {health_data['active_conversations']}")
                return True
            else:
                print("❌ HumAIne-chatbot is not responding")
                return False
        except Exception as e:
            print(f"❌ Error connecting to HumAIne-chatbot: {e}")
            return False
    
    def start_conversation(self, user_id=None):
        """Start a new conversation"""
        if not user_id:
            user_id = input("Enter user ID (or press Enter for default): ").strip()
            if not user_id:
                user_id = f"cli_user_{int(time.time())}"
        
        try:
            response = requests.post(f"{BASE_URL}/conversation/start", 
                                  json={"user_id": user_id})
            if response.status_code == 200:
                data = response.json()
                self.session_id = data['session_id']
                self.user_id = user_id
                self.conversation_active = True
                print(f"✅ Conversation started!")
                print(f"   Session ID: {self.session_id}")
                print(f"   User ID: {self.user_id}")
                return True
            else:
                print(f"❌ Failed to start conversation: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error starting conversation: {e}")
            return False
    
    def send_message(self, message):
        """Send a message to the chatbot"""
        if not self.conversation_active:
            print("❌ No active conversation. Start one first!")
            return False
        
        try:
            payload = {
                "session_id": self.session_id,
                "message": message,
                "typing_start_time": int(time.time() * 1000) - 5000,
                "typing_end_time": int(time.time() * 1000) - 1000
            }
            
            response = requests.post(f"{BASE_URL}/conversation/message", json=payload)
            if response.status_code == 200:
                data = response.json()
                
                # Print the response
                print(f"\n🤖 Bot Response:")
                print(f"{'='*60}")
                print(data['response'])
                print(f"{'='*60}")
                
                # Print personalization info
                params = data['metadata']['personalization_params']
                print(f"\n📊 Personalization:")
                print(f"   Style: {params['response_style']}")
                print(f"   Detail: {params['detail_level']}")
                print(f"   Complexity: {params['language_complexity']}")
                print(f"   User Type: {params['user_type']}")
                print(f"   Engagement: {params['engagement_level']}")
                
                return True
            else:
                print(f"❌ Failed to send message: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False
    
    def get_user_profile(self):
        """Get current user profile"""
        if not self.user_id:
            print("❌ No user ID available")
            return False
        
        try:
            response = requests.get(f"{BASE_URL}/user/{self.user_id}/profile")
            if response.status_code == 200:
                profile = response.json()
                print(f"\n📊 User Profile for {self.user_id}:")
                print(f"{'='*60}")
                print(json.dumps(profile, indent=2))
                return True
            else:
                print(f"❌ Failed to get profile: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error getting profile: {e}")
            return False
    
    def end_conversation(self):
        """End the current conversation"""
        if not self.conversation_active:
            print("❌ No active conversation to end")
            return False
        
        try:
            response = requests.post(f"{BASE_URL}/conversation/end", 
                                  json={"session_id": self.session_id})
            if response.status_code == 200:
                data = response.json()
                print(f"\n📈 Conversation Summary:")
                print(f"{'='*60}")
                print(f"Session Duration: {data['session_data']['session_duration']}ms")
                print(f"Engagement Time: {data['session_data']['engagement']['engagement_time']}ms")
                print(f"Total Turns: {data['session_data']['feedback']['total_bot_messages_count']}")
                
                self.conversation_active = False
                self.session_id = None
                return True
            else:
                print(f"❌ Failed to end conversation: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error ending conversation: {e}")
            return False
    
    def show_help(self):
        """Show available commands"""
        print(f"\n📋 Available Commands:")
        print(f"{'='*60}")
        print(f"health          - Check if chatbot is running")
        print(f"start [user_id] - Start a new conversation")
        print(f"send <message>  - Send a message to the bot")
        print(f"profile         - Show current user profile")
        print(f"end             - End current conversation")
        print(f"help            - Show this help")
        print(f"quit/exit       - Exit the CLI")
        print(f"{'='*60}")
    
    def run(self):
        """Run the interactive CLI"""
        print("🚀 HumAIne-chatbot CLI")
        print("="*60)
        print("Type 'help' for available commands")
        print("Type 'quit' or 'exit' to leave")
        print("="*60)
        
        while True:
            try:
                command = input("\n🤖 HumAIne> ").strip()
                
                if not command:
                    continue
                
                parts = command.split()
                cmd = parts[0].lower()
                
                if cmd in ['quit', 'exit']:
                    if self.conversation_active:
                        print("⚠️  Ending active conversation...")
                        self.end_conversation()
                    print("👋 Goodbye!")
                    break
                
                elif cmd == 'help':
                    self.show_help()
                
                elif cmd == 'health':
                    self.check_health()
                
                elif cmd == 'start':
                    user_id = parts[1] if len(parts) > 1 else None
                    self.start_conversation(user_id)
                
                elif cmd == 'send':
                    if len(parts) < 2:
                        print("❌ Usage: send <message>")
                        continue
                    message = ' '.join(parts[1:])
                    self.send_message(message)
                
                elif cmd == 'profile':
                    self.get_user_profile()
                
                elif cmd == 'end':
                    self.end_conversation()
                
                else:
                    print(f"❌ Unknown command: {cmd}")
                    print("Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Main function"""
    cli = HumAIChatbotCLI()
    
    # Check if chatbot is running
    if not cli.check_health():
        print("❌ Cannot connect to HumAIne-chatbot. Make sure it's running!")
        sys.exit(1)
    
    # Run the CLI
    cli.run()

if __name__ == "__main__":
    main() 