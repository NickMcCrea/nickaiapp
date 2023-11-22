import React, { useEffect } from 'react';
import ReactFlow, {
  Background,
  useNodesState,
  useEdgesState,
  Node,
  Edge,
  Position,
  Controls
} from 'react-flow-renderer';

export interface PipelineStep {
  id: string;
  action: string;
  params: any; // Adjust as per your actual param structure
}

interface PipelineVisualiserProps {
  pipelineDefinition: PipelineStep[];
}


interface ColorMapping {
  [action: string]: string;
}

const PipelineVisualiser: React.FC<PipelineVisualiserProps> = ({ pipelineDefinition }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  const getColorForAction = (action: string): string => {
    const colorMapping: ColorMapping = {
      'load_from_service': '#0D9CD9',  // Deep Sky Blue
      'filter': '#DAA520',             // Goldenrod
      'join': '#228B22',               // Forest Green
      'select_columns': '#A52A2A',     // Brown
      'aggregate': '#6A5ACD',          // Slate Blue
      'sort': '#FF4500',               // Orange Red
      'transform': '#2F4F4F',          // Dark Slate Gray
      'persist': '#8B4513',             // Saddle Brown
      // Add more actions and their corresponding colors here
    };
    return colorMapping[action] || '#95A3AB'; // Default color if action not found
  };
  
  

  useEffect(() => {
    const convertToFlowElements = (pipeline: PipelineStep[]): void => {
      const horizontalSpacing = 250; // Adjust spacing between nodes
      let yOffset = 100;
      let xOffset = 0;
  
      const newNodes: Node[] = [];
      const loadNodes: Node[] = [];
      const otherNodes: Node[] = [];
      const newEdges: Edge[] = [];
  
      // Separate load events and other events into different arrays
      pipeline.forEach((step, index) => {
        const node = {
          id: step.id,
          type: 'default',
          data: { 
            label: (
              <>
                <strong>Action:</strong> {step.action}
                <br />
                <strong>Params:</strong> {JSON.stringify(step.params, null, 2)}
              </>
            )
          },
          sourcePosition: Position.Right,
          targetPosition: Position.Left,
          position: { x: xOffset, y: yOffset }, // This will be adjusted later
          style: { 
            backgroundColor: getColorForAction(step.action),
            color: '#fff',
            border: '1px solid #333',
            boxShadow: '0 2px 10px rgba(0,0,0,0.15)'
          }
        };
  
        if (step.action === 'load_from_service') {
          loadNodes.push(node);
          xOffset += horizontalSpacing; // Increment x position for next load node
        } else {
          otherNodes.push(node);
        }
      });
  
      // Set positions for load nodes at the top
      loadNodes.forEach((node, index) => {
        node.position = { x: index * horizontalSpacing, y: 50 };
        newNodes.push(node);
      });
  
      // Set positions for other nodes and create edges
      otherNodes.forEach((node, index) => {
        node.position = { x: index * horizontalSpacing, y: 250 }; // Adjust y position for other nodes
        newNodes.push(node);
        if (index > 0) {
          newEdges.push({
            id: `e${otherNodes[index - 1].id}-${node.id}`,
            source: otherNodes[index - 1].id,
            target: node.id,
            animated: true,
            style: { stroke: '#333', strokeWidth: 2 },
           // arrowHeadType: 'arrowclosed',
          });
        }
      });
  
      setNodes(newNodes);
      setEdges(newEdges);
    };
  
    convertToFlowElements(pipelineDefinition);
  }, [pipelineDefinition, setNodes, setEdges]);
  

  return (
    <div style={{ height: 900 }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
      >
    
      </ReactFlow>
    </div>
  );
};

export default PipelineVisualiser;
