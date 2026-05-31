"""
Password Strength Analyzer - Comprehensive Password Security Evaluation Tool
"""

import re
import math
import random
import string
from typing import Dict, Tuple, List
from dataclasses import dataclass
from enum import Enum


class StrengthLevel(Enum):
    """Password strength classification"""
    VERY_WEAK = "Very Weak"
    WEAK = "Weak"
    FAIR = "Fair"
    GOOD = "Good"
    STRONG = "Strong"
    VERY_STRONG = "Very Strong"


@dataclass
class PasswordAnalysis:
    """Container for password analysis results"""
    password: str
    score: int
    strength_level: StrengthLevel
    issues: List[str]
    suggestions: List[str]
    entropy: float
    feedback: str


class PasswordStrengthAnalyzer:
    """
    Comprehensive password strength analyzer with entropy calculation,
    complexity checking, and intelligent suggestions.
    """
    
    # Common weak patterns
    COMMON_PATTERNS = {
        r'123456': 'Sequential numbers',
        r'qwerty': 'Keyboard pattern',
        r'password': 'Common word',
        r'abc123': 'Sequential alphanumeric',
        r'admin': 'Default username',
        r'letmein': 'Common phrase',
        r'welcome': 'Common word',
        r'monkey': 'Common word',
    }
    
    # Common passwords database (simplified)
    COMMON_PASSWORDS = {
        'password', 'password123', 'admin', 'letmein', 'welcome',
        'monkey', '123456', 'qwerty', 'abc123', '111111',
        'dragon', 'master', 'prince', 'princess', 'starwars'
    }
    
    def __init__(self):
        """Initialize analyzer with default configuration"""
        self.min_length = 8
        self.min_entropy = 60  # bits
        
    def analyze(self, password: str) -> PasswordAnalysis:
        """
        Perform comprehensive password analysis
        
        Args:
            password: Password string to analyze
            
        Returns:
            PasswordAnalysis object with detailed metrics
        """
        issues = self._check_issues(password)
        score = self._calculate_score(password, issues)
        strength_level = self._get_strength_level(score)
        entropy = self._calculate_entropy(password)
        suggestions = self._generate_suggestions(password, issues)
        feedback = self._generate_feedback(strength_level, entropy)
        
        return PasswordAnalysis(
            password=password,
            score=score,
            strength_level=strength_level,
            issues=issues,
            suggestions=suggestions,
            entropy=entropy,
            feedback=feedback
        )
    
    def _check_issues(self, password: str) -> List[str]:
        """
        Identify security issues with the password
        
        Args:
            password: Password to check
            
        Returns:
            List of identified issues
        """
        issues = []
        
        # Length check
        if len(password) < self.min_length:
            issues.append(f"Too short (min {self.min_length} characters)")
        
        # Character complexity checks
        if not re.search(r'[a-z]', password):
            issues.append("No lowercase letters")
        if not re.search(r'[A-Z]', password):
            issues.append("No uppercase letters")
        if not re.search(r'\d', password):
            issues.append("No numbers")
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
            issues.append("No special characters")
        
        # Pattern checks
        for pattern, description in self.COMMON_PATTERNS.items():
            if re.search(pattern, password, re.IGNORECASE):
                issues.append(f"Contains {description}")
        
        # Common password check
        if password.lower() in self.COMMON_PASSWORDS:
            issues.append("Password is too common")
        
        # Repetitive character check
        if re.search(r'(.)\1{2,}', password):
            issues.append("Contains repeating characters")
        
        # Sequential character check
        if self._has_sequential_chars(password):
            issues.append("Contains sequential characters")
        
        return issues
    
    def _has_sequential_chars(self, password: str, length: int = 3) -> bool:
        """
        Check for sequential characters (abc, 123, etc.)
        
        Args:
            password: Password to check
            length: Sequence length to detect
            
        Returns:
            True if sequential characters found
        """
        for i in range(len(password) - length + 1):
            substring = password[i:i+length]
            
            # Check numeric sequence
            if substring.isdigit():
                if int(substring[1]) - int(substring[0]) == 1 and \
                   int(substring[2]) - int(substring[1]) == 1:
                    return True
            
            # Check alphabetic sequence
            if substring.isalpha():
                if ord(substring[1]) - ord(substring[0]) == 1 and \
                   ord(substring[2]) - ord(substring[1]) == 1:
                    return True
        
        return False
    
    def _calculate_score(self, password: str, issues: List[str]) -> int:
        """
        Calculate password strength score (0-100)
        
        Args:
            password: Password to score
            issues: List of identified issues
            
        Returns:
            Score between 0-100
        """
        score = 50  # Base score
        
        # Length bonus
        score += min(len(password) - self.min_length, 20)
        
        # Character variety bonus
        variety_score = 0
        if re.search(r'[a-z]', password):
            variety_score += 5
        if re.search(r'[A-Z]', password):
            variety_score += 5
        if re.search(r'\d', password):
            variety_score += 5
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
            variety_score += 10
        
        score += variety_score
        
        # Issue penalties
        score -= len(issues) * 5
        
        # Entropy bonus
        entropy = self._calculate_entropy(password)
        if entropy > 100:
            score += 10
        elif entropy > 80:
            score += 5
        
        # Cap score at 100
        return min(max(score, 0), 100)
    
    def _calculate_entropy(self, password: str) -> float:
        """
        Calculate password entropy in bits
        
        Entropy = log2(character_space_size ^ password_length)
        
        Args:
            password: Password to analyze
            
        Returns:
            Entropy in bits
        """
        character_space = 0
        
        if re.search(r'[a-z]', password):
            character_space += 26
        if re.search(r'[A-Z]', password):
            character_space += 26
        if re.search(r'\d', password):
            character_space += 10
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
            character_space += 32
        
        if character_space == 0:
            return 0
        
        entropy = len(password) * math.log2(character_space)
        return round(entropy, 2)
    
    def _get_strength_level(self, score: int) -> StrengthLevel:
        """
        Determine strength level based on score
        
        Args:
            score: Password score (0-100)
            
        Returns:
            StrengthLevel enum value
        """
        if score < 20:
            return StrengthLevel.VERY_WEAK
        elif score < 40:
            return StrengthLevel.WEAK
        elif score < 60:
            return StrengthLevel.FAIR
        elif score < 75:
            return StrengthLevel.GOOD
        elif score < 90:
            return StrengthLevel.STRONG
        else:
            return StrengthLevel.VERY_STRONG
    
    def _generate_suggestions(self, password: str, issues: List[str]) -> List[str]:
        """
        Generate intelligent suggestions for improvement
        
        Args:
            password: Original password
            issues: List of identified issues
            
        Returns:
            List of suggestions
        """
        suggestions = []
        
        if "Too short" in issues:
            suggestions.append(f"Increase length to at least {self.min_length} characters")
        
        if "No uppercase letters" in issues:
            suggestions.append("Add uppercase letters (A-Z)")
        
        if "No lowercase letters" in issues:
            suggestions.append("Add lowercase letters (a-z)")
        
        if "No numbers" in issues:
            suggestions.append("Add numbers (0-9)")
        
        if "No special characters" in issues:
            suggestions.append("Add special characters (!@#$%^&*)")
        
        if any("repeating" in issue.lower() for issue in issues):
            suggestions.append("Avoid repeating characters")
        
        if any("sequential" in issue.lower() for issue in issues):
            suggestions.append("Avoid sequential characters (abc, 123)")
        
        # Generate strong password suggestions
        if len(issues) > 0:
            strong_password = self._generate_strong_password()
            suggestions.append(f"Try this strong password: {strong_password}")
        
        return suggestions
    
    def _generate_strong_password(self, length: int = 16) -> str:
        """
        Generate a strong random password
        
        Args:
            length: Desired password length
            
        Returns:
            Strong password string
        """
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Ensure at least one of each character type
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special)
        ]
        
        # Fill remaining length with random characters
        all_chars = lowercase + uppercase + digits + special
        password += [random.choice(all_chars) for _ in range(length - len(password))]
        
        # Shuffle to avoid predictable pattern
        random.shuffle(password)
        return ''.join(password)
    
    def _generate_feedback(self, strength_level: StrengthLevel, entropy: float) -> str:
        """
        Generate human-readable feedback
        
        Args:
            strength_level: Password strength level
            entropy: Entropy in bits
            
        Returns:
            Feedback string
        """
        feedback = f"Strength: {strength_level.value} | Entropy: {entropy} bits\n"
        
        if entropy < self.min_entropy:
            feedback += "⚠️  WARNING: Low entropy - password may be vulnerable to brute force attacks\n"
        
        if strength_level in [StrengthLevel.VERY_WEAK, StrengthLevel.WEAK]:
            feedback += "🔴 Consider creating a stronger password"
        elif strength_level in [StrengthLevel.FAIR, StrengthLevel.GOOD]:
            feedback += "🟡 Password is acceptable but could be improved"
        elif strength_level in [StrengthLevel.STRONG, StrengthLevel.VERY_STRONG]:
            feedback += "🟢 Good password! Secure for most purposes"
        
        return feedback
    
    def check_breach(self, password: str) -> Tuple[bool, str]:
        """
        Check if password appears in breach databases (simulated)
        
        Args:
            password: Password to check
            
        Returns:
            Tuple of (is_breached, message)
        """
        # In production, integrate with Have I Been Pwned API
        if password.lower() in self.COMMON_PASSWORDS:
            return True, "⚠️  This password has been found in breach databases!"
        return False, "✅ Password not found in known breach databases"
    
    def batch_analyze(self, passwords: List[str]) -> List[PasswordAnalysis]:
        """
        Analyze multiple passwords
        
        Args:
            passwords: List of passwords to analyze
            
        Returns:
            List of PasswordAnalysis objects
        """
        return [self.analyze(pwd) for pwd in passwords]


def print_analysis(analysis: PasswordAnalysis) -> None:
    """
    Pretty-print password analysis results
    
    Args:
        analysis: PasswordAnalysis object to print
    """
    print(f"\n{'='*60}")
    print(f"Password Analysis Report")
    print(f"{'='*60}")
    print(f"Password: {'*' * len(analysis.password)}")
    print(f"Score: {analysis.score}/100")
    print(f"Strength: {analysis.strength_level.value}")
    print(f"Entropy: {analysis.entropy} bits")
    
    if analysis.issues:
        print(f"\n❌ Issues Found ({len(analysis.issues)}):")
        for issue in analysis.issues:
            print(f"  • {issue}")
    else:
        print(f"\n✅ No issues found!")
    
    if analysis.suggestions:
        print(f"\n💡 Suggestions ({len(analysis.suggestions)}):")
        for suggestion in analysis.suggestions:
            print(f"  • {suggestion}")
    
    print(f"\n{analysis.feedback}")
    print(f"{'='*60}\n")


def main():
    """Main execution"""
    analyzer = PasswordStrengthAnalyzer()
    
    # Test passwords
    test_passwords = [
        "password123",
        "MyP@ssw0rd!",
        "aB1!cD2@eF3#",
        "SuperSecurePassword123!@#",
        "abc123",
        "P@ssw0rd!X9$mK2#vL5&oQ7*"
    ]
    
    print("\n🔐 PASSWORD STRENGTH ANALYZER - BATCH TEST\n")
    
    for pwd in test_passwords:
        analysis = analyzer.analyze(pwd)
        print_analysis(analysis)
        
        # Check breach database
        is_breached, message = analyzer.check_breach(pwd)
        print(f"Breach Check: {message}\n")


if __name__ == "__main__":
    main()
