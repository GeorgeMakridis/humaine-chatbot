"""
Profile Persistence for HumAIne-chatbot

This module handles saving and loading user profiles to/from disk
for persistence across server restarts.
"""

import json
import os
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from ..models.schemas import UserProfile

class ProfilePersistence:
    """Handles profile persistence to/from disk"""
    
    def __init__(self, profiles_dir: str = "data/profiles"):
        self.profiles_dir = Path(profiles_dir)
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
    
    def save_profile(self, user_id: str, profile: UserProfile) -> bool:
        """Save a user profile to disk"""
        try:
            profile_file = self.profiles_dir / f"{user_id}.json"
            
            # Convert profile to dict, handling datetime objects
            profile_dict = self._profile_to_dict(profile)
            
            with open(profile_file, 'w') as f:
                json.dump(profile_dict, f, indent=2, default=str)
            
            return True
        except Exception as e:
            print(f"❌ Failed to save profile for user {user_id}: {e}")
            return False
    
    def load_profile(self, user_id: str) -> Optional[UserProfile]:
        """Load a user profile from disk"""
        try:
            profile_file = self.profiles_dir / f"{user_id}.json"
            
            if not profile_file.exists():
                return None
            
            with open(profile_file, 'r') as f:
                profile_dict = json.load(f)
            
            # Convert dict back to UserProfile object
            return self._dict_to_profile(profile_dict)
            
        except Exception as e:
            print(f"❌ Failed to load profile for user {user_id}: {e}")
            return None
    
    def load_all_profiles(self) -> Dict[str, UserProfile]:
        """Load all profiles from disk"""
        profiles = {}
        
        try:
            for profile_file in self.profiles_dir.glob("*.json"):
                user_id = profile_file.stem
                profile = self.load_profile(user_id)
                if profile:
                    profiles[user_id] = profile
        except Exception as e:
            print(f"❌ Failed to load profiles: {e}")
        
        return profiles
    
    def delete_profile(self, user_id: str) -> bool:
        """Delete a user profile from disk"""
        try:
            profile_file = self.profiles_dir / f"{user_id}.json"
            if profile_file.exists():
                profile_file.unlink()
                return True
            return False
        except Exception as e:
            print(f"❌ Failed to delete profile for user {user_id}: {e}")
            return False
    
    def _profile_to_dict(self, profile: UserProfile) -> Dict[str, Any]:
        """Convert UserProfile object to dictionary"""
        profile_dict = profile.__dict__.copy()
        
        # Handle datetime objects
        if 'created_at' in profile_dict and profile_dict['created_at']:
            profile_dict['created_at'] = profile_dict['created_at'].isoformat()
        if 'updated_at' in profile_dict and profile_dict['updated_at']:
            profile_dict['updated_at'] = profile_dict['updated_at'].isoformat()
        
        return profile_dict
    
    def _dict_to_profile(self, profile_dict: Dict[str, Any]) -> UserProfile:
        """Convert dictionary back to UserProfile object"""
        # Handle datetime conversion
        if 'created_at' in profile_dict and profile_dict['created_at']:
            try:
                profile_dict['created_at'] = datetime.fromisoformat(profile_dict['created_at'])
            except:
                profile_dict['created_at'] = datetime.utcnow()
        
        if 'updated_at' in profile_dict and profile_dict['updated_at']:
            try:
                profile_dict['updated_at'] = datetime.fromisoformat(profile_dict['updated_at'])
            except:
                profile_dict['updated_at'] = datetime.utcnow()
        
        # Create UserProfile object
        profile = UserProfile(
            user_id=profile_dict.get('user_id', ''),
            created_at=profile_dict.get('created_at', datetime.utcnow()),
            updated_at=profile_dict.get('updated_at', datetime.utcnow())
        )
        
        # Update all attributes
        for key, value in profile_dict.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        return profile
    
    def get_profile_stats(self) -> Dict[str, Any]:
        """Get statistics about stored profiles"""
        try:
            profile_files = list(self.profiles_dir.glob("*.json"))
            total_profiles = len(profile_files)
            
            # Calculate total size
            total_size = sum(f.stat().st_size for f in profile_files)
            
            return {
                "total_profiles": total_profiles,
                "total_size_bytes": total_size,
                "profiles_directory": str(self.profiles_dir.absolute()),
                "last_updated": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "error": str(e),
                "profiles_directory": str(self.profiles_dir.absolute())
            }
