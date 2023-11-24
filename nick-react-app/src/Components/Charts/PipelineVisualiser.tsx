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
      'add_columns': '#6A5ACD',       // Slate Blue
      'apply_conditional_logic': '#FF8C00', // Dark Orange
      // Add more actions and their corresponding colors here
    };
    return colorMapping[action] || '#95A3AB'; // Default color if action not found
  };



  useEffect(() => {
    const convertToFlowElements = (pipeline: PipelineStep[]): void => {
      const horizontalSpacing = 250; // Adjust spacing between nodes
      let xPos = 0;

      const newNodes: Node[] = [];
      const newEdges: Edge[] = [];
      // Determine if the node is a data source node
    
      pipeline.forEach((step, index) => {

        const isDataSourceNode = step.action === 'load_from_service';

        // Create action node
        newNodes.push({
          id: step.id,
          type: 'default',
          data: {
            label: step.action === 'load_from_service' ? step.params.data_source_name : (
              <>
                <strong>Action:</strong> {step.action}
                <br />
                <strong>Params:</strong> {JSON.stringify(step.params, null, 2)}
              </>
            )
          },
          sourcePosition: Position.Right,
          targetPosition: Position.Left,
          position: { x: xPos, y: 100 },
          style: {
            backgroundColor: getColorForAction(step.action),
            color: '#fff', // Set text color to white
            border: '1px solid #333',
            boxShadow: '0 2px 10px rgba(0,0,0,0.15)',
            ...(isDataSourceNode ? { width: 180, height: 50, fontSize: 16 } : {}), // Example size, adjust as needed
          }
        });

        // Increment x position after the load action node
        
          xPos += horizontalSpacing;
        

        // Special case for the first load action to connect directly to the next action
        if (index === 0 && step.action === 'load_from_service' && pipeline.length > 1) {
          const nextStep = pipeline[1]; // Assuming there's at least one more step
          newEdges.push({
            id: `e${step.id}-${nextStep.id}`,
            source: step.id,
            target: nextStep.id,
            animated: true,
            style: { stroke: '#333', strokeWidth: 2 },

          });
        }

        // If this is not a load action, increment x position for the data set node


        // Link this action node to the previous data set node, if this is not the first node
        if (index > 0) {
          const previousDataSetNodeId = `${pipeline[index - 1].id}-data-set`;
          newEdges.push({
            id: `e${previousDataSetNodeId}-${step.id}`,
            source: previousDataSetNodeId,
            target: step.id,
            animated: true,
            style: { stroke: '#333', strokeWidth: 2 }
          });
        }

        // Create data set node after non-load actions
        if (step.action !== 'load_from_service') {
          const dataSetNodeId = `${step.id}-data-set`;

          newNodes.push({
            id: dataSetNodeId,
            type: 'default',
            data: { label: step.params.name },
            position: { x: xPos, y: 100 },
            sourcePosition: Position.Right,
            targetPosition: Position.Left,
            style: {
              backgroundColor: '#0D9CD9',
              color: '#fff', // Set text color to white
              border: '1px solid #333',
              boxShadow: '0 2px 10px rgba(0,0,0,0.15)',
              width: 180, // Example size, adjust as needed
              height: 50, // Example size, adjust as needed
              //text size
              fontSize: 14,

            }
          });

          // Create edge between action node and data set node
          newEdges.push({
            id: `e${step.id}-${dataSetNodeId}`,
            source: step.id,
            target: dataSetNodeId,
            animated: true,
            style: { stroke: '#333', strokeWidth: 2 }
          });

          // Increment x position for the next node
          xPos += horizontalSpacing;
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