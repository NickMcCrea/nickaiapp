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
import dagre from 'dagre';


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
      'data_frame': '#C39BD3',        
      // Add more actions and their corresponding colors here
    };
    return colorMapping[action] || '#95A3AB'; // Default color if action not found
  };

  const applyDagreLayout = (nodes: Node[], edges: Edge[]) => {
    const g = new dagre.graphlib.Graph();
    g.setGraph({ rankdir: 'LR', ranksep: 100, nodesep: 50 }); // Customize these values as needed
    g.setDefaultEdgeLabel(() => ({}));
  
    nodes.forEach(node => {
      g.setNode(node.id, { width: 150, height: 200 }); // Adjust size as per your node's dimensions
    });
  
    edges.forEach(edge => {
      g.setEdge(edge.source, edge.target);
    });
  
    dagre.layout(g);
  
    return nodes.map(node => {
      const nodeWithPosition = g.node(node.id);
      return {
        ...node,
        position: {
          x: nodeWithPosition.x - nodeWithPosition.width / 2,
          y: nodeWithPosition.y - nodeWithPosition.height / 2
        }
      };
    });
  };
  



  useEffect(() => {
    const convertToFlowElements = (pipeline: PipelineStep[]): void => {
      
      let xPosLoadFromService = 0;
      let yPosLoadFromService = 0;
      let xPos = 450;
      let yPos = 0;
      let horizontalSpacing= 400;
      let verticalSpacing = 200;



      const newNodes: Node[] = [];
      const newEdges: Edge[] = [];
      // Determine if the node is a data source node

      //how many load_from_service nodes are there?
      let loadFromServiceNodeCount = 0;
      pipeline.forEach((step, index) => {
        if (step.action === 'load_from_service') {
          loadFromServiceNodeCount++;
        }
      });

      //set the yPos to be the middle of the canvas
      yPos = (loadFromServiceNodeCount * verticalSpacing) / 3;
   
      pipeline.forEach((step, index) => {

        newNodes.push({
          id: step.id,
          type: 'default',
          position: step.action === 'load_from_service' ? { x: xPosLoadFromService, y: yPosLoadFromService } : { x: xPos, y: yPos },
          
          data: {
            label: (
              <>
               <strong>{step.action.toUpperCase()}</strong> 
                <br />
                <br />
               {JSON.stringify(step.params, null, 2)}
              </>
            )
          },
         
          sourcePosition: Position.Right,
          targetPosition: Position.Left,
          style: { background: getColorForAction(step.action), color: 'white' },
        });

        
       if (step.action === 'load_from_service') {
        

        //create a node for the output of the load_from_service node
          newNodes.push({
            id: step.params.output_name,
            type: 'default',
            position: { x: xPosLoadFromService+200, y: yPosLoadFromService },
            data: {
              label: (
                <>
                  <strong>{step.params.output_name}</strong>
                </>
              )
            },
            sourcePosition: Position.Right,
            targetPosition: Position.Left,
            style: { background: getColorForAction('data_frame'), color: 'white' },
          });

          //create an edge between the load_from_service node and the output node
          newEdges.push({
            id: `e${index}-1`,
            source: step.id,
            target: step.params.output_name,
            animated: true,
            style: { stroke: '#333', strokeWidth: 2 },
          });
         

          yPosLoadFromService += verticalSpacing;

        }
        else {

          newNodes.push({
            id: step.params.output_name,
            type: 'default',
            position: { x: xPos+200, y: yPos },
            data: {
              label: (
                <>
                  <strong>{step.params.output_name}</strong>
                </>
              )
            },
            sourcePosition: Position.Right,
            targetPosition: Position.Left,
            style: { background: getColorForAction('data_frame'), color: 'white' },
          });
          xPos += horizontalSpacing;
        }

        //create an edge between the current node and the output node
        newEdges.push({
          id: `e${index}-2`,
          source: step.id,
          target: step.params.output_name,
          animated: true,
          style: { stroke: '#333', strokeWidth: 2 },
        });

        //create an edge between the node and its input node
        
        newEdges.push({
          id: `e${index}-3`,
          source: step.params.name,
          target: step.id,
          animated: true,
          style: { stroke: '#333', strokeWidth: 2 },
        });

        //if you're a join node
        if (step.action === 'join') {
          //create an edge between the node and its second input node
          newEdges.push({
            id: `e${index}-4`,
            source: step.params.other_name,
            target: step.id,
            animated: true,
            style: { stroke: '#333', strokeWidth: 2 },
          });
        }
        

      });

      const laidOutNodes = applyDagreLayout(newNodes, newEdges);
      setNodes(laidOutNodes);
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


