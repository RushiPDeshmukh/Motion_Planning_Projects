function isReached = isGoal(obj, goalState, newState)
%EXAMPLEHELPERGOALFUNC

isReached = false;
if abs(newState(1) < goalState(1)) < 0.01 && ...
    abs(newState(2) < goalState(2)) < 0.01 && ...
    abs(newState(3) < goalState(3)) < 0.01 && ...
    abs(newState(4) < goalState(4)) < 0.01 && ...
    abs(newState(5) < goalState(5)) < 0.01 && ...
    abs(newState(6) < goalState(6)) < 0.01 && ...
     abs(newState(7) < goalState(7)) < 0.01 %#ok<*ELARLOG>
    isReached = true;
end

end
