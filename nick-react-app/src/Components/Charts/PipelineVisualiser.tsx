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

      const newNodes: Node[] = pipeline.map((step, index) => ({
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
        position: { x: index * horizontalSpacing, y: 100 }, // Adjust for horizontal layout
        style: { 
          backgroundColor: getColorForAction(step.action),
          color: '#fff',
          border: '1px solid #333',
          boxShadow: '0 2px 10px rgba(0,0,0,0.15)'
        }
      }));

      const newEdges: Edge[] = newNodes.slice(1).map((node, i) => ({
        id: `e${newNodes[i].id}-${node.id}`,
        source: newNodes[i].id,
        target: node.id,
        animated: true,
        style: { stroke: '#333', strokeWidth: 2 },
        arrowHeadType: 'arrowclosed',
        // ... existing edge properties ...
      }));

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
