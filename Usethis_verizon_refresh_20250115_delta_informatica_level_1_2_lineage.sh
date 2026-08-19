#!/bin/bash
currentdate=$(TZ=Asia/Kolkata date +"%Y%m%d%I%M%p")
sh /eagle/00_vz_refresh/neo4j_TD_ref-ASMT/bin/cypher-shell -a localhost:5011 -u neo4j -p root "
CALL apoc.export.csv.query(\"
match(j:job)-[:refers]->(c:code)-[rc:refers]->(c1:code)-[rn:refers]->(n:workflow)-[:refers]->(t:task)-[r2:refers]->(d:dataMapping)-[r4:refers{writes:true}]->(trg:dataEntity)-[:dependsOn]->(s:dataEntity)<-[r5:refers{reads:true}]-(d) where not j.product in ['PMF','GLU'] and not (n)<-[:refers]-(:task) and r2.calledVia contains n.name and r4.calledVia contains n.name and r5.calledVia contains n.name and 
r2.calledVia contains j.name and r4.calledVia contains j.name and r5.calledVia contains j.name and
rc.calledVia contains j.name and rn.calledVia contains j.name and
n.product='informatica' 
optional match(t)-[:triggers]->(st:task)
optional match(t)<-[:triggers]-(pt:task)
RETURN
distinct j.product as jobproduct,j.location as joblocation,j.name as JobName,
c.location as MainScipt_Location,c.name as MainScipt,
c1.location as Child_code_location,c1.name as Child_Code_Name,
 n.REPO as repo_name,n.location as folder, n.name as workflow_name,null as worklet_location,null as worklet_name,t.name as session_name,coalesce(st.name,null) as successor_task,coalesce(pt.name,null) as predecessor_task,d.name as mapping_name,trg.product as tagret_product,trg.schema as target_schema,trg.name as target_name,trg.location as target_file,DataEntity.entityType(trg) as target_type,s.product as source_product,s.schema as source_schema,s.name as source_name,s.location as source_file,DataEntity.entityType(s) as source_type

union

match(j:job)-[:refers]->(c:code)-[rc:refers]->(c1:code)-[rn:refers]->(n:workflow)-[:refers]->(t:task)-[r2:refers]->(d:dataMapping)-[r4:refers{writes:true,reads:true}]->(trg:dataEntity)-[:dependsOn]->(trg) where not j.product in ['PMF','GLU'] and not (n)<-[:refers]-(:task) and r2.calledVia contains n.name and r4.calledVia contains n.name  and
r2.calledVia contains j.name and r4.calledVia contains j.name  and 
rc.calledVia contains j.name and rn.calledVia contains j.name and
 n.product='informatica' 
optional match(t)-[:triggers]->(st:task)
optional match(t)<-[:triggers]-(pt:task)
RETURN
distinct j.product as jobproduct,j.location as joblocation,j.name as JobName,
c.location as MainScipt_Location,c.name as MainScipt,
c1.location as Child_code_location,c1.name as Child_Code_Name,
 n.REPO as repo_name,n.location as folder, n.name as workflow_name,null as worklet_location,null as worklet_name,t.name as session_name,coalesce(st.name,null) as successor_task,coalesce(pt.name,null) as predecessor_task,d.name as mapping_name,trg.product as tagret_product,trg.schema as target_schema,trg.name as target_name,trg.location as target_file,DataEntity.entityType(trg) as target_type,trg.product as source_product,trg.schema as source_schema,trg.name as source_name,trg.location as source_file,DataEntity.entityType(trg) as source_type

union

//-----------------------------OnlY for target

match(j:job)-[:refers]->(c:code)-[rc:refers]->(c1:code)-[rn:refers]->(n:workflow)-[:refers]->(t:task)-[r2:refers]->(d:dataMapping)-[r4:refers{writes:true}]->(trg:dataEntity) where not (n)<-[:refers]-(:task) and r2.calledVia contains n.name and r4.calledVia contains n.name  and
rc.calledVia contains j.name and rn.calledVia contains j.name and  r2.calledVia contains j.name and r4.calledVia contains j.name and
 n.product='informatica' and not (d)-[:refers{reads:true}]->(:dataEntity)<-[:dependsOn]-(trg) 
RETURN
distinct  j.product as jobproduct,j.location as joblocation,j.name as JobName,
c.location as MainScipt_Location,c.name as MainScipt,
c1.location as Child_code_location,c1.name as Child_Code_Name,
 n.REPO as repo_name,n.location as folder, n.name as workflow_name,null as worklet_location,null as worklet_name,t.name as session_name,null as successor_task,null as predecessor_task,d.name as mapping_name,trg.product as tagret_product,trg.schema as target_schema,trg.name as target_name,trg.location as target_file,DataEntity.entityType(trg) as target_type,null as source_product,null as source_schema,null as source_name,null as source_file,null as source_type

union
//-----------------------------OnlY for source

match(j:job)-[:refers]->(c:code)-[rc:refers]->(c1:code)-[rn:refers]->(n:workflow)-[:refers]->(t:task)-[r2:refers]->(d:dataMapping)-[r4:refers{reads:true}]->(trg:dataEntity) where not (n)<-[:refers]-(:task) and r2.calledVia contains n.name and r4.calledVia contains n.name  and
rn.calledVia contains j.name and  r2.calledVia contains j.name and r4.calledVia contains j.name and
 n.product='informatica' and not (d)-[:refers{writes:true}]->(:dataEntity)-[:dependsOn]->(trg)
RETURN
distinct  j.product as jobproduct,j.location as joblocation,j.name as JobName,
c.location as MainScipt_Location,c.name as MainScipt,
c1.location as Child_code_location,c1.name as Child_Code_Name, n.REPO as repo_name,n.location as folder, n.name as workflow_name,null as worklet_location,null as worklet_name,t.name as session_name,null as successor_task,null as predecessor_task,d.name as mapping_name,
null as tagret_product,null as target_schema,null as target_name,null as target_file,null as target_type,
trg.product as source_product,trg.schema as source_schema,trg.name as source_name,trg.location as source_file,DataEntity.entityType(trg) as source_type


union
///////////////////////level 2 added ////////////////////////////////

match(j:job)-[:refers]->(c:code)-[rc:refers]->(n:workflow)-[:refers]->(t:task)-[r3:refers]->(w1:workflow)-[r1:refers]->(t1:task)-[r2:refers]->(d:dataMapping)-[r4:refers{writes:true}]->(trg:dataEntity)-[:dependsOn]->(s:dataEntity)<-[r5:refers{reads:true}]-(d) where not j.product in ['PMF','GLU'] and r1.calledVia contains n.name and r2.calledVia contains n.name and r3.calledVia contains n.name and r4.calledVia contains n.name and r5.calledVia contains n.name and
r1.calledVia contains j.name and r2.calledVia contains j.name and r3.calledVia contains j.name and r4.calledVia contains j.name and r5.calledVia contains j.name and rc.calledVia contains j.name and 
 n.product='informatica'
optional match(t1)-[:triggers]->(st:task)
optional match(t1)<-[:triggers]-(pt:task)
RETURN
distinct  j.product as jobproduct,j.location as joblocation,j.name as JobName,
c.location as MainScipt_Location,c.name as MainScipt,
c.location as Child_code_location,c.name as Child_Code_Name,
n.REPO as repo_name, n.location as folder, n.name as workflow_name,w1.location as worklet_location,w1.name as worklet_name,t1.name as session_name,coalesce(st.name,null) as successor_task,coalesce(pt.name,null) as predecessor_task, d.name as mapping_name,trg.product as tagret_product,trg.schema as target_schema,trg.name as target_name,trg.location as target_file,DataEntity.entityType(trg) as target_type,s.product as source_product,s.schema as source_schema,s.name as source_name,s.location as source_file,DataEntity.entityType(s) as source_type

union

match(j:job)-[:refers]->(c:code)-[rc:refers]->(n:workflow)-[:refers]->(t:task)-[r3:refers]->(w1:workflow)-[r1:refers]->(t1:task)-[r2:refers]->(d:dataMapping)-[r4:refers{writes:true,reads:true}]->(trg:dataEntity)-[:dependsOn]->(trg) where not j.product in ['PMF','GLU'] and r1.calledVia contains n.name and r2.calledVia contains n.name and r3.calledVia contains n.name and r4.calledVia contains n.name and 
r1.calledVia contains j.name and r2.calledVia contains j.name and r3.calledVia contains j.name and r4.calledVia contains j.name and 
rc.calledVia contains j.name and 
n.product='informatica'
optional match(t1)-[:triggers]->(st:task)
optional match(t1)<-[:triggers]-(pt:task)
RETURN
distinct j.product as jobproduct,j.location as joblocation,j.name as JobName,
c.location as MainScipt_Location,c.name as MainScipt,
c.location as Child_code_location,c.name as Child_Code_Name,
 n.REPO as repo_name,n.location as folder, n.name as workflow_name,w1.location as worklet_location,w1.name as worklet_name,t1.name as session_name,coalesce(st.name,null) as successor_task,coalesce(pt.name,null) as predecessor_task,d.name as mapping_name,trg.product as tagret_product,trg.schema as target_schema,trg.name as target_name,trg.location as target_file,DataEntity.entityType(trg) as target_type,trg.product as source_product,trg.schema as source_schema,trg.name as source_name,trg.location as source_file,DataEntity.entityType(trg) as source_type
 
union

match(j:job)-[:refers]->(c:code)-[rc:refers]->(n:workflow)-[:refers]->(t:task)-[r2:refers]->(d:dataMapping)-[r4:refers{writes:true}]->(trg:dataEntity)-[:dependsOn]->(s:dataEntity)<-[r5:refers{reads:true}]-(d) where not j.product in ['PMF','GLU'] and not (n)<-[:refers]-(:task) and r2.calledVia contains n.name and r4.calledVia contains n.name and r5.calledVia contains n.name and 
r2.calledVia contains j.name and r4.calledVia contains j.name and r5.calledVia contains j.name and
rc.calledVia contains j.name and 
n.product='informatica' 
optional match(t)-[:triggers]->(st:task)
optional match(t)<-[:triggers]-(pt:task)
RETURN
distinct j.product as jobproduct,j.location as joblocation,j.name as JobName,
c.location as MainScipt_Location,c.name as MainScipt,
c.location as Child_code_location,c.name as Child_Code_Name,
 n.REPO as repo_name,n.location as folder, n.name as workflow_name,null as worklet_location,null as worklet_name,t.name as session_name,coalesce(st.name,null) as successor_task,coalesce(pt.name,null) as predecessor_task,d.name as mapping_name,trg.product as tagret_product,trg.schema as target_schema,trg.name as target_name,trg.location as target_file,DataEntity.entityType(trg) as target_type,s.product as source_product,s.schema as source_schema,s.name as source_name,s.location as source_file,DataEntity.entityType(s) as source_type
 
union

match(j:job)-[:refers]->(c:code)-[rc:refers]->(n:workflow)-[:refers]->(t:task)-[r2:refers]->(d:dataMapping)-[r4:refers{writes:true,reads:true}]->(trg:dataEntity)-[:dependsOn]->(trg) where not j.product in ['PMF','GLU'] and not (n)<-[:refers]-(:task) and r2.calledVia contains n.name and r4.calledVia contains n.name  and
r2.calledVia contains j.name and r4.calledVia contains j.name  and 
rc.calledVia contains j.name and 
 n.product='informatica' 
optional match(t)-[:triggers]->(st:task)
optional match(t)<-[:triggers]-(pt:task)
RETURN
distinct j.product as jobproduct,j.location as joblocation,j.name as JobName,
c.location as MainScipt_Location,c.name as MainScipt,
c.location as Child_code_location,c.name as Child_Code_Name,
 n.REPO as repo_name,n.location as folder, n.name as workflow_name,null as worklet_location,null as worklet_name,t.name as session_name,coalesce(st.name,null) as successor_task,coalesce(pt.name,null) as predecessor_task,d.name as mapping_name,trg.product as tagret_product,trg.schema as target_schema,trg.name as target_name,trg.location as target_file,DataEntity.entityType(trg) as target_type,trg.product as source_product,trg.schema as source_schema,trg.name as source_name,trg.location as source_file,DataEntity.entityType(trg) as source_type

///level-3

union 

match(j:job)-[:refers]->(c:code)-[rc:refers]->(n:workflow)-[r7:refers]->(t:task)-[r6:refers]->(w:workflow)-[r5:refers]->(t1:task)-[r4:refers]->(w1:workflow)-[r3:refers]->(t2:task)-[r2:refers]->(d:dataMapping)-[r1:refers{writes:true}]->(trg:dataEntity)-[:dependsOn]->(s:dataEntity)<-[r:refers{reads:true}]-(d) where r.calledVia contains n.name  and r1.calledVia contains n.name and r2.calledVia contains n.name and r3.calledVia contains n.name and r4.calledVia contains n.name and r5.calledVia contains n.name and r6.calledVia contains n.name and
r.calledVia contains j.name  and r1.calledVia contains j.name and r2.calledVia contains j.name and r3.calledVia contains j.name and r4.calledVia contains j.name and r5.calledVia contains j.name and r6.calledVia contains j.name and not j.product in ['PMF','GLU'] and
rc.calledVia contains j.name and 
 n.product='informatica'
optional match(t2)-[:triggers]->(st:task)
optional match(t2)<-[:triggers]-(pt:task)
RETURN distinct  j.product as jobproduct,j.location as joblocation,j.name as JobName,
c.location as MainScipt_Location,c.name as MainScipt,
c.location as Child_code_location,c.name as Child_Code_Name,
 n.REPO as repo_name, n.location as folder, n.name as workflow_name,w.location as worklet_location,w.name as worklet_name,t2.name as session_name,coalesce(st.name,null) as successor_task,coalesce(pt.name,null) as predecessor_task,d.name as mapping_name,trg.product as tagret_product,trg.schema as target_schema,trg.name as target_name,trg.location as target_file,DataEntity.entityType(trg) as target_type,s.product as source_product,s.schema as source_schema,s.name as source_name,s.location as source_file,DataEntity.entityType(s) as source_type

union

match(j:job)-[:refers]->(c:code)-[rc:refers]->(n:workflow)-[r7:refers]->(t:task)-[r6:refers]->(w:workflow)-[r5:refers]->(t1:task)-[r4:refers]->(w1:workflow)-[r3:refers]->(t2:task)-[r2:refers]->(d:dataMapping)-[r1:refers{writes:true,reads:true}]->(trg:dataEntity)-[:dependsOn]->(trg) where   r1.calledVia contains n.name and r2.calledVia contains n.name and r3.calledVia contains n.name and r4.calledVia contains n.name and r5.calledVia contains n.name and r6.calledVia contains n.name and 
r1.calledVia contains j.name and r2.calledVia contains j.name and r3.calledVia contains j.name and r4.calledVia contains j.name and r5.calledVia contains j.name and r6.calledVia contains j.name and not j.product in ['PMF','GLU'] and
rc.calledVia contains j.name and 
n.product='informatica'
optional match(t2)-[:triggers]->(st:task)
optional match(t2)<-[:triggers]-(pt:task)
RETURN distinct  j.product as jobproduct,j.location as joblocation,j.name as JobName,
c.location as MainScipt_Location,c.name as MainScipt,
c.location as Child_code_location,c.name as Child_Code_Name,
 n.REPO as repo_name,n.location as folder, n.name as workflow_name,w.location as worklet_location,w.name as worklet_name,t2.name as session_name,coalesce(st.name,null) as successor_task,coalesce(pt.name,null) as predecessor_task,d.name as mapping_name,trg.product as tagret_product,trg.schema as target_schema,trg.name as target_name,trg.location as target_file,DataEntity.entityType(trg) as target_type,trg.product as source_product,trg.schema as source_schema,trg.name as source_name,trg.location as source_file,DataEntity.entityType(trg) as source_type

union

//level-4
match(j:job)-[:refers]->(c:code)-[rc:refers]->(n:workflow)-[r9:refers]->(t:task)-[r8:refers]->(w:workflow)-[r7:refers]->(t1:task)-[r6:refers]->(w1:workflow)-[r5:refers]->(t2:task)-[r4:refers]->(w2:workflow)-[r3:refers]->(t3:task)-[r2:refers]->(d:dataMapping)-[r1:refers{writes:true}]->(trg:dataEntity)-[:dependsOn]->(s:dataEntity)<-[r:refers{reads:true}]-(d) where r.calledVia contains n.name and
r1.calledVia contains n.name and r2.calledVia contains n.name and r3.calledVia contains n.name and r4.calledVia contains n.name and r5.calledVia contains n.name and r6.calledVia contains n.name and r7.calledVia contains n.name and r8.calledVia contains n.name and
r.calledVia contains j.name and
r1.calledVia contains j.name and r2.calledVia contains j.name and r3.calledVia contains j.name and r4.calledVia contains j.name and r5.calledVia contains j.name and r6.calledVia contains j.name and r7.calledVia contains j.name and r8.calledVia contains j.name
 and not j.product in ['PMF','GLU']
 and rc.calledVia contains j.name and  n.product='informatica' 
optional match(t3)-[:triggers]->(st:task)
optional match(t3)<-[:triggers]-(pt:task)
RETURN
distinct  j.product as jobproduct,j.location as joblocation,j.name as JobName,
c.location as MainScipt_Location,c.name as MainScipt,
c.location as Child_code_location,c.name as Child_Code_Name,
 n.REPO as repo_name, n.location as folder, n.name as workflow_name,w.location as worklet_location,w.name as worklet_name,t3.name as session_name,coalesce(st.name,null) as successor_task,coalesce(pt.name,null) as predecessor_task,d.name as mapping_name,trg.product as tagret_product,trg.schema as target_schema,trg.name as target_name,trg.location as target_file,DataEntity.entityType(trg) as target_type,s.product as source_product,s.schema as source_schema,s.name as source_name,s.location as source_file,DataEntity.entityType(s) as source_type

union

match(j:job)-[:refers]->(c:code)-[rc:refers]->(n:workflow)-[r9:refers]->(t:task)-[r8:refers]->(w:workflow)-[r7:refers]->(t1:task)-[r6:refers]->(w1:workflow)-[r5:refers]->(t2:task)-[r4:refers]->(w2:workflow)-[r3:refers]->(t3:task)-[r2:refers]->(d:dataMapping)-[r1:refers{writes:true,reads:true}]->(trg:dataEntity)-[:dependsOn]->(trg) where
r1.calledVia contains n.name and r2.calledVia contains n.name and r3.calledVia contains n.name and r4.calledVia contains n.name and r5.calledVia contains n.name and r6.calledVia contains n.name and r7.calledVia contains n.name and r8.calledVia contains n.name and
r1.calledVia contains j.name and r2.calledVia contains j.name and r3.calledVia contains j.name and r4.calledVia contains j.name and r5.calledVia contains j.name and r6.calledVia contains j.name and r7.calledVia contains j.name and r8.calledVia contains j.name
and not j.product in ['PMF','GLU'] and rc.calledVia contains j.name and  
n.product='informatica' 
optional match(t3)-[:triggers]->(st:task)
optional match(t3)<-[:triggers]-(pt:task)
RETURN
distinct  j.product as jobproduct,j.location as joblocation,j.name as JobName,
c.location as MainScipt_Location,c.name as MainScipt,
c.location as Child_code_location,c.name as Child_Code_Name,
 n.REPO as repo_name,n.location as folder, n.name as workflow_name,w.location as worklet_location,w.name as worklet_name,t3.name as session_name,coalesce(st.name,null) as successor_task,coalesce(pt.name,null) as predecessor_task,d.name as mapping_name,trg.product as tagret_product,trg.schema as target_schema,trg.name as target_name,trg.location as target_file,DataEntity.entityType(trg) as target_type,trg.product as source_product,trg.schema as source_schema,trg.name as source_name,trg.location as source_file,DataEntity.entityType(trg) as source_type


union 

//-----------------------------OnlY for target

match(j:job)-[:refers]->(c:code)-[rc:refers]->(n:workflow)-[:refers]->(t:task)-[r2:refers]->(d:dataMapping)-[r4:refers{writes:true}]->(trg:dataEntity) where not (n)<-[:refers]-(:task) and r2.calledVia contains n.name and r4.calledVia contains n.name  and
rc.calledVia contains j.name and  r2.calledVia contains j.name and r4.calledVia contains j.name and
 n.product='informatica' and not (d)-[:refers{reads:true}]->(:dataEntity)<-[:dependsOn]-(trg) 
RETURN
distinct  j.product as jobproduct,j.location as joblocation,j.name as JobName,
c.location as MainScipt_Location,c.name as MainScipt,
c.location as Child_code_location,c.name as Child_Code_Name,
 n.REPO as repo_name,n.location as folder, n.name as workflow_name,null as worklet_location,null as worklet_name,t.name as session_name,null  as successor_task,null as predecessor_task, d.name as mapping_name,trg.product as tagret_product,trg.schema as target_schema,trg.name as target_name,trg.location as target_file,DataEntity.entityType(trg) as target_type,null as source_product,null as source_schema,null as source_name,null as source_file,null as source_type




// -----------------------------OnlY for source
union 
match(j:job)-[:refers]->(c:code)-[rc:refers]->(n:workflow)-[:refers]->(t:task)-[r2:refers]->(d:dataMapping)-[r4:refers{reads:true}]->(trg:dataEntity) where not (n)<-[:refers]-(:task) and r2.calledVia contains n.name and r4.calledVia contains n.name and  r2.calledVia contains j.name and r4.calledVia contains j.name and rc.calledVia contains j.name and
 n.product='informatica' and not (d)-[:refers{writes:true}]->(:dataEntity)-[:dependsOn]->(trg) RETURN
distinct  j.product as jobproduct,j.location as joblocation,j.name as JobName,
c.location as MainScipt_Location,c.name as MainScipt,
c.location as Child_code_location,c.name as Child_Code_Name, n.REPO as repo_name,n.location as folder, n.name as workflow_name,null as worklet_location,null as worklet_name,t.name as session_name,null  as successor_task,null as predecessor_task,d.name as mapping_name,
null as tagret_product,null as target_schema,null as target_name,null as target_file,null as target_type,
trg.product as source_product,trg.schema as source_schema,trg.name as source_name,trg.location as source_file,DataEntity.entityType(trg) as source_type




\",'${currentdate}_overall_informatica_level_1_2_lineage.csv', {delim: '|'})"
