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
      let yPos = 300;
      let xPosData = 100;


      const newNodes: Node[] = [];
      const newEdges: Edge[] = [];
      // Determine if the node is a data source node
      let firstNonDataSourceNode = true;

      pipeline.forEach((step, index) => {

        //if the pipeline step action is load_from_service, create at teh top of the graph
        if (step.action === 'load_from_service') {

          //add a new node
          newNodes.push({
            id: step.id + '-data-source',
            type: 'input',
            position: { x: xPosData, y: 0 },
            data: { label: step.params.data_source_name },
            style: { background: getColorForAction(step.action), color: 'white' },
          });

          xPosData += horizontalSpacing;

        }

        if (step.action !== 'load_from_service') {

          //add a node to the left, using the input data source name of this step

          //is this the first step that is not a data source?
          if (firstNonDataSourceNode) {

            createDataSourceNode(newNodes, step.id + '-left',step.params.name, step, xPos, yPos, getColorForAction);
            firstNonDataSourceNode = false;
          }

          xPos += horizontalSpacing;

          //add a new node
          newNodes.push({
            id: step.id,
            type: 'default',
            position: { x: xPos, y: yPos },
            data: { label: step.action },
            sourcePosition: Position.Right,
            targetPosition: Position.Left,
            style: { background: getColorForAction(step.action), color: 'white' },
          });

          //if we're a join action, create a data source ABOVE the join node
          if (step.action === 'join') {
            
            createDataSourceNode(newNodes, step.id + '-join',step.params.other_name, step, xPos, yPos-100, getColorForAction);
  
          }



          xPos += horizontalSpacing;

          //add a node to the left, using the input data source name of this step
          createDataSourceNode(newNodes, step.id + '-right',step.params.name, step, xPos, yPos, getColorForAction);
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

function createDataSourceNode(newNodes: Node<any>[], id: string, label:string, step: PipelineStep, xPos: number, yPos: number, getColorForAction: (action: string) => string) {
  newNodes.push({
    id: id,
    type: 'default',
    position: { x: xPos, y: yPos },
    data: { label: label },
    sourcePosition: Position.Right,
    targetPosition: Position.Left,
    style: { background: getColorForAction('load_from_service'), color: 'white' },
  });
}
