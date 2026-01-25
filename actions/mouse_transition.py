from actions.mouse_action import MouseAction
from pynput.mouse import Controller
import random
import math
import time


class MouseTransition(MouseAction):
    """Smoothly transition mouse cursor from current position to target using Bezier curves.
    
    Creates natural, human-like mouse movement with:
    - Curved path (not straight line)
    - Variable speed (slow at start/end, faster in middle)
    - Micro jitter for realism
    
    Attributes:
        target_x (int): Target x-coordinate.
        target_y (int): Target y-coordinate.
        duration (float): Approximate duration of the transition in seconds.
        curve_intensity (float): How curved the path should be (0.0-1.0).
        add_jitter (bool): Whether to add small random movements.
    """

    def __init__(self, target_x: int, target_y: int, duration: float = None, curve_intensity: float = 0.3, add_jitter: bool = True) -> None:
        """Initialize transition with target coordinates and movement parameters."""
        self.target_x = target_x
        self.target_y = target_y
        self.duration = duration
        self.curve_intensity = curve_intensity
        self.add_jitter = add_jitter

    def __str__(self) -> str:
        return f"Transition: -> ({self.target_x}, {self.target_y})"

    def _cubic_bezier(self, t: float, p0: tuple, p1: tuple, p2: tuple, p3: tuple) -> tuple:
        """Calculate point on cubic Bézier curve at parameter t (0-1)."""
        x = (
            (1 - t) ** 3 * p0[0] +
            3 * (1 - t) ** 2 * t * p1[0] +
            3 * (1 - t) * t ** 2 * p2[0] +
            t ** 3 * p3[0]
        )
        y = (
            (1 - t) ** 3 * p0[1] +
            3 * (1 - t) ** 2 * t * p1[1] +
            3 * (1 - t) * t ** 2 * p2[1] +
            t ** 3 * p3[1]
        )
        return (x, y)

    def _ease_in_out(self, t: float) -> float:
        """Easing function: slow at start and end, fast in middle."""
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2

    def _generate_control_points(self, start: tuple, end: tuple) -> tuple:
        """Generate random control points for Bézier curve to create natural arc."""
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Perpendicular direction for curve offset
        if distance > 0:
            perp_x = -dy / distance
            perp_y = dx / distance
        else:
            perp_x, perp_y = 0, 0
        
        curve_offset = distance * self.curve_intensity * random.uniform(-1, 1)
        
        cp1_x = start[0] + dx * 0.3 + perp_x * curve_offset * random.uniform(0.5, 1.0)
        cp1_y = start[1] + dy * 0.3 + perp_y * curve_offset * random.uniform(0.5, 1.0)
        
        cp2_x = start[0] + dx * 0.7 + perp_x * curve_offset * random.uniform(0.5, 1.0)
        cp2_y = start[1] + dy * 0.7 + perp_y * curve_offset * random.uniform(0.5, 1.0)
        
        return ((cp1_x, cp1_y), (cp2_x, cp2_y))

    def _calculate_duration(self, distance: float) -> float:
        """Calculate appropriate duration based on distance (Fitts's Law inspired)."""
        if self.duration is not None:
            return self.duration

        base_duration = 0.1 + (distance / 1000) * 0.5
        base_duration *= random.uniform(0.8, 1.2)
        return max(0.05, min(0.8, base_duration))

    def execute(self) -> None:
        """Perform the natural mouse transition."""
        mouse = Controller()
        start_pos = mouse.position
        end_pos = (self.target_x, self.target_y)
        
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Skip if already at target
        if distance < 1:
            return
        
        cp1, cp2 = self._generate_control_points(start_pos, end_pos)

        duration = self._calculate_duration(distance)
        
        # More steps = smoother movement
        steps = max(10, int(distance / 3))
        step_delay = duration / steps
        
        for i in range(1, steps + 1):
            linear_t = i / steps
            eased_t = self._ease_in_out(linear_t)
            
            point = self._cubic_bezier(eased_t, start_pos, cp1, cp2, end_pos)
            
            if self.add_jitter and i < steps:
                jitter_amount = max(0, 2 - (i / steps) * 2) 
                point = (
                    point[0] + random.uniform(-jitter_amount, jitter_amount),
                    point[1] + random.uniform(-jitter_amount, jitter_amount)
                )
            
            mouse.position = (int(point[0]), int(point[1]))
            time.sleep(step_delay)
        
        mouse.position = end_pos


def calculate_transition_needed(current_pos: tuple, next_action, threshold: int = 1) -> MouseTransition | None:
    """Check if a transition is needed before the next action.
    
    Args:
        current_pos: Current cursor position (x, y).
        next_action: The next action to be executed.
        threshold: Minimum distance in pixels to trigger transition.
    
    Returns:
        MouseTransition if needed, None otherwise.
    """
    target_pos = None
    
    action_type = type(next_action).__name__
    
    if action_type == 'MouseClick':
        target_pos = (next_action.x, next_action.y)
    elif action_type == 'MouseMoveClick':
        target_pos = (next_action.x, next_action.y)
    elif action_type == 'MouseMove':
        target_pos = (next_action.x, next_action.y)
    elif action_type == 'MouseDrag':
        target_pos = (next_action.x, next_action.y)
    elif action_type == 'MousePath':
        if next_action.points:
            first_point = next_action.points[0]
            target_pos = (first_point[0], first_point[1])
    
    if target_pos is None:
        return None
    
    dx = target_pos[0] - current_pos[0]
    dy = target_pos[1] - current_pos[1]
    distance = math.sqrt(dx * dx + dy * dy)
    
    if distance > threshold:
        return MouseTransition(target_pos[0], target_pos[1])
    
    return None


def get_action_end_position(action) -> tuple | None:
    """Get the expected cursor position after an action completes.
    
    Args:
        action: The action to check.
    
    Returns:
        Tuple (x, y) of expected end position, or None if unknown.
    """
    action_type = type(action).__name__
    
    if action_type == 'MouseClick':
        return (action.x, action.y)
    elif action_type == 'MouseMoveClick':
        return (action.x, action.y)
    elif action_type == 'MouseMove':
        return (action.x, action.y)
    elif action_type == 'MouseDrag':
        return (action.x, action.y)
    elif action_type == 'MousePath':
        if action.points:
            last_point = action.points[-1]
            return (last_point[0], last_point[1])
    elif action_type == 'MouseTransition':
        return (action.target_x, action.target_y)
    
    return None
