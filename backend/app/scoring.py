from typing import Dict

class ConnectionScorer:
    def __init__(self):
        self.title_keywords = {
            'CEO': 10,
            'CTO': 9,
            'Director': 8,
            'Manager': 7,
            'Lead': 6,
            'Senior': 5,
            'Engineer': 4
        }
        
        self.company_weights = {
            'FAANG': 10,
            'Fortune500': 8,
            'Startup': 6
        }
        
    def score_title(self, title: str) -> int:
        score = 0
        title = title.lower()
        
        for keyword, weight in self.title_keywords.items():
            if keyword.lower() in title:
                score += weight
                
        return score
    
    def score_message(self, message: str) -> int:
        if not message:
            return 0
            
        score = 0
        # Basic scoring for personalized messages
        if len(message) > 50:
            score += 5
        if '@' in message or 'name' in message.lower():
            score += 3
            
        return score
    
    def calculate_score(self, connection: Dict) -> int:
        title_score = self.score_title(connection['title'])
        message_score = self.score_message(connection['message'])
        
        total_score = title_score + message_score
        return min(100, total_score)  # Cap score at 100 