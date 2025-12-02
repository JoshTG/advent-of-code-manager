from dataclasses import dataclass


@dataclass
class Log:
  """Simple dataclass for storing one log line in context"""
  data: any
  label: str = ''
  level: str = ''

  def print(self):
    """Prints the log in context"""
    print(f'[{self.level}:{self.label}] {str(self.data)}')
