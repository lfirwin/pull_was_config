#-----------------------------------------------------------------------------------------
# This Jython script is used to gather different WAS configuration information from a
# target environment.
#
# The following parameters are required in order:
#      environment name - used for naming the associated html file
#      title - title to use in the html file
#      host - fqdn of the host
#      port - the ssl port for the WAS console
#      bin - location of the bin directory from which to run the wsadmin.sh command
#-----------------------------------------------------------------------------------------

# Import system modules
import sys
import java.io as javaio
import md5

# Define the lineSeparator for this environment
lineSeparator = java.lang.System.getProperty('line.separator')

# JVM Properties Dictionary
jvmProperties = ['initialHeapSize:Min Heap Size',
'maximumHeapSize:Max Heap Size',
'verboseModeGarbageCollection:Verbose GC',
'genericJvmArguments:Generic JVM Arguments']

# DataSource Properties Dictionary
dbDataSourceProperties = {"name":"Name",
"jndiName":"JNDI Name",
"providerType":"JDBC Provider Type",
"datasourceHelperClassname":"Data Source Helper Class",
"description":"Description",
"authDataAlias":"Authentication Alia",
"xaRecoveryAuthAlias":"XA Recovery Authentication Alias",
"statementCacheSize":"Statement Cache Size"}

# Resource Properties Dictionary
dbResourceProperties = {"URL":"URL",
"databaseName":"Database Name",
"serverName":"Server Name",
"portNumber":"Port Number"}

# Connection Pool Properties Dictionary
connPoolProperties = {'maxConnections':'Max Connections',
'minConnections':'Min Connections',
'agedTimeout':'Aged Timeout',
'connectionTimeout':'Connection Timeout',
'reapTime':'Reap Time',
'unusedTimeout':'Unused Timeout',
'purgePolicy':'Purge Policy'}

# JVM Thread Pool Properties Dictionary
jvmThreadPoolProperties = {"minimumSize":"minimum",
"maximumSize":"maximum"}

# Session Management Properties Dictionary
tuningParamsProperties = {'invalidationTimeout':'Session Timeout',
"maxInMemorySessionCount":"Max In-Memory Session Count"}

# MQ Connection Factory Properties Dictionary
mqCFProperties = {'jndiName':'JNDI Name',
'queueManager':'QMGR Name',
'host':'QMGR Host Name',
'port':'QMGR Port Number', 
'channel':'QMGR Server Conn Channel', 
'transportType':'Transport Type',
'XAEnabled':'Enable XA'}

# Activation Spec Properties
actSpecProperties = {'description':'Description',
'jndiName':'JNDI Name'}

# Activation Spec Resource Properties
actSpecResourceProperties = {'queueManager':'QMGR Name',
'hostName':'QMGR Host Name',
'port':'QMGR Port Number', 
'channel':'QMGR Server Conn Channel', 
'transportType':'Transport Type',
'destination':'Destination JNDI Name',
'destinationType':'Destination Type'}

# J2C Connection Factory Properties
j2cCFProperties = {'description':'Description',
'jndiName':'JNDI Name'}

# J2C Connection Factory Resource Properties
j2cCFResourceProperties = {'BusName':'Bus Name',
'ConnectionProximity':'Connection Proximity',
'TargetSignificance':'Target Significance',
'TargetType':'Target Type'}

# MQ Queue Properties
mqQueueProperties = {'name':'Name',
'jndiName':'JNDI Name',
'baseQueueManagerName':'QMGR Name',
'baseQueueName':'Queue Name'}

# J2C Queue Properties
j2cQueueProperties = {'description':'Description',
'jndiName':'JNDI Name'}

# J2C Queue Resource Properties
j2cQueueResourceProperties = {'BusName':'Bus Name',
'QueueName':'Queue Name'}

# Function - Define scope of the cell
def buildScopes (scopes):
   # Add the Cell to the scopes list
   scopes.append("cell:" +  AdminControl.getCell())

   # Build the App Server and Web Server lists for later use
   app_servers = []
   web_servers = []
   servers = AdminConfig.list("Server").splitlines()
   for server in servers:
      server_type = AdminConfig.showAttribute(server, 'serverType')
      if server_type == "APPLICATION_SERVER":
         app_servers.append(server.split("(")[0])
      elif server_type == "WEB_SERVER":
         web_servers.append("web_server:" + server.split("(")[0])

   # Add Clusters and Cluster Members to the Scopes list
   clusters = AdminConfig.list("ServerCluster").splitlines()   
   for cluster in clusters:
      scopes.append("cluster:" + cluster.split("(")[0])
      members = AdminConfig.showAttribute(cluster, "members")[1:-1].split()
      for member in members:
         mem_name = member.split("(")[0]
         scopes.append("cluster_member:" + mem_name)
         del app_servers[app_servers.index(mem_name)]

   # Add Nodes and their associated App Servers that are not members of a Cluster
   # to the Scopes list
   nodes = AdminConfig.list("Node").splitlines()
   for node in nodes:
      node_name = node.split("(")[0]
      scopes.append("node:" + node_name)
      found = None
      for app_server in app_servers:
         if AdminConfig.getid("/Node:" + node_name + "/Server:" + app_server + "/"):
            found = "y"
            try:
               i = scopes.index("app_server:" + app_server + ",node:" + node_name)
            except ValueError:
               scopes.append("app_server:" + app_server + ",node:" + node_name)

   # Add the Web Server list to the Scopes list
   if len(web_servers):
      scopes.extend(web_servers)

# Function - Build initial HTML 
def buildHeader (env, console, scopes):
   html = "<!DOCTYPE html>" + lineSeparator
   html = html + "<html>" + lineSeparator

   # Head section with links to CSS files and javascript files, page title, and
   # embedded javascript
   html = html + "<head>" + lineSeparator
   html = html + "<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\"/>" + lineSeparator
   html = html + "<link rel=\"stylesheet\" href=\"mktree.css\" type=\"text/css\"/>" + lineSeparator
   html = html + "<script type=\"text/javascript\" src=\"mktree.js\"></script>" + lineSeparator
   html = html + "<title>" + env + "</title>" + lineSeparator
   html = html + "<script>" + lineSeparator
   html = html + "function myFunction()" + lineSeparator
   html = html + "{" + lineSeparator
   html = html + "expandTree('cell')" + lineSeparator
   html = html + "}" + lineSeparator
   html = html + "</script>" + lineSeparator
   html = html + "</head>" + lineSeparator
   
   # Body section beginning
   html = html + "<body onload=\"myFunction()\">" + lineSeparator
   html = html + "<a id=\"top\"></a>" + lineSeparator
   html = html + "<div class=\"update\">" + lineSeparator
   html = html + "<a class=\"home\" href=\"./index.html\">Home</a><br/>" + lineSeparator
   html = html + "Updated:" + lineSeparator
   html = html + "<script>" + lineSeparator
   html = html + "document.write(document.lastModified);" + lineSeparator
   html = html + "</script>" + lineSeparator
   html = html + "</div>" + lineSeparator
   html = html + "<h3>" + env + ": <a href=\"" + console + "\" target=\"_blank\">" + console + "</a></h3>" + lineSeparator

   # Navigation bar division - if adding a new section add a link here
   html = html + "<div id=\"navcontainer\">" + lineSeparator
   html = html + "<ul>" + lineSeparator
   html = html + "<li><a href=\"#scope\">Scope</a></li>" + lineSeparator
   html = html + "<li><a href=\"#server_config\">Server Configurations</a></li>" + lineSeparator
   html = html + "<li><a href=\"#datasources\">Data Sources</a></li>" + lineSeparator
   html = html + "<li><a href=\"#mqcf\">MQ Conn Factories</a></li>" + lineSeparator
   html = html + "<li><a href=\"#mqqueue\">MQ Queues</a></li>" + lineSeparator
   html = html + "<li><a href=\"#j2cconn\">J2C Conn Factories</a></li>" + lineSeparator
   html = html + "<li><a href=\"#j2cqueue\">J2C Queues</a></li>" + lineSeparator
   html = html + "</ul>" + lineSeparator
   html = html + "<br/>" + lineSeparator
   html = html + "<ul>" + lineSeparator
   html = html + "<li><a href=\"#actspecs\">Activation Specs</a></li>" + lineSeparator
   html = html + "<li><a href=\"#rees\">REEs</a></li>" + lineSeparator
   html = html + "<li><a href=\"#urls\">URLs</a></li>" + lineSeparator
   html = html + "<li><a href=\"#libraries\">Shared Libraries</a></li>" + lineSeparator
   html = html + "<li><a href=\"#variables\">Variables</a></li>" + lineSeparator
   html = html + "<li><a href=\"#vhosts\">Virtual Hosts</a></li>" + lineSeparator
   html = html + "</ul>" + lineSeparator
   html = html + "</div>" + lineSeparator

   return html
   
   
def indent(level):
   return " " * (2 * level)

# Function - Build the TreeView List
def buildTreeView(fileOutputStreamXML, env, console, scopes, rees, rees_props, urls, dss, libraries, variables, mqcfIds, actSpecs, j2cConnIds, mqQueues, j2cQueues):
   # Start the TreeView with the Cell
   cell = scopes[0].split(":")[1]

   html = "<h4><a id=\"scope\"></a>Scope</h4>" + lineSeparator
   html = html + "<ul class=\"mktree\" id=\"cell\">" + lineSeparator
   html = html + "  <li>Cell: " + cell + lineSeparator
   html = html + "    <ul>" + lineSeparator
   html = html + "      <li><a href=\"#vhosts\">Virtual Hosts</a></li>" + lineSeparator
   level = 1

   fileOutputStreamXML.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + lineSeparator)
   fileOutputStreamXML.write("<?xml-stylesheet type=\"text/xsl\" href=\"wpp-config.xsl\"?>" + lineSeparator)
   fileOutputStreamXML.write("<cell name=\"" + cell + "\">" + lineSeparator)
   fileOutputStreamXML.write(indent(level) + "<env>" + env + "</env>" + lineSeparator)
   fileOutputStreamXML.write(indent(level) + "<console>" + console + "</console>" + lineSeparator)
   fileOutputStreamXML.write(buildVirtualHostsXML(level))

   # Check for configuration items at the Cell level and create a link if they exist
   # REEs
   id, entries = findConfigIds("cell", cell, rees)
   if id:
      html = html + "      <li><a href=\"#" + id + "\">REEs</a></li>" + lineSeparator 
      found_props = []
      for ree in entries:
         found_props.append(rees_props[rees.index(ree)])
      fileOutputStreamXML.write(buildREEXML(level, entries, found_props))

   # URLs
   id, entries = findConfigIds("cell", cell, urls)
   if id:
      html = html + "      <li><a href=\"#" + id + "\">URLs</a></li>" + lineSeparator
      fileOutputStreamXML.write(buildURLXML(level, entries))

   # Data Sources
   id, entries = findConfigIds("cell", cell, dss)
   if id:
      html = html + "      <li><a href=\"#" + id + "\">Data Sources</a></li>" + lineSeparator
      fileOutputStreamXML.write(buildDataSourceXML(level, entries))

   # MQ Connection Factories
   id, entries = findConfigIds("cell", cell, mqcfIds)
   if id:
      html = html + "      <li><a href=\"#" + id + "\">MQ Connection Factories</a></li>" + lineSeparator
      fileOutputStreamXML.write(buildMQCFXML(level, entries))

   # MQ Queues
   id, entries = findConfigIds("cell", cell, mqQueues)
   if id:
      html = html + "      <li><a href=\"#" + id + "\">MQ Queues</a></li>" + lineSeparator
      fileOutputStreamXML.write(buildMQQueueXML(level, entries))

   # JDC Connection Factories
   id, entries = findConfigIds("cell", cell, j2cConnIds)
   if id:
      html = html + "      <li><a href=\"#" + id + "\">J2C Connection Factories</a></li>" + lineSeparator
      fileOutputStreamXML.write(buildJ2CCFXML(level, entries))

   # J2C Queues
   id, entries = findConfigIds("cell", cell, j2cQueues)
   if id:
      html = html + "      <li><a href=\"#" + id + "\">J2C Queues</a></li>" + lineSeparator
      fileOutputStreamXML.write(buildJ2CQueueXML(level, entries))
      
   # Activation Specifications
   id, entries = findConfigIds("cell", cell, actSpecs)
   if id:
      html = html + "      <li><a href=\"#" + id + "\">Activation Specs</a></li>" + lineSeparator
      fileOutputStreamXML.write(buildActSpecXML(level, entries))
      
   # Shared Libraries
   id, entries = findConfigIds("cell", cell, libraries)
   if id:
      html = html + "      <li><a href=\"#" + id + "\">Shared Libraries</a></li>" + lineSeparator
      fileOutputStreamXML.write(buildSharedLibrariesXML(level, entries))
      
   # Variables
   id, entries = findConfigIds("cell", cell, variables)
   if id:
      html = html + "      <li><a href=\"#" + id + "\">Variables</a></li>" + lineSeparator
      fileOutputStreamXML.write(buildVariablesXML(level, entries))

   # Process all subsequent scope entries
   i = 1
   node = "" 
   web_server = ""
   node_close = ""
   clusters = ""
   while i < len(scopes):
      # Get the type (cluster, cluster_member, node, app_server, web_server)
      type = scopes[i].split(":")[0]
      print type

      if type == "cluster":
         # Add the cluster name to the TreeView list
         cluster_index = i
         cluster_name = scopes[i].split(":")[1]
         if i == 1:
            html = html + "      <li>Clusters" + lineSeparator
            fileOutputStreamXML.write(indent(level) + "<clusters>" + lineSeparator)
            level = 2
            clusters = "true"
         html = html + "        <ul>" + lineSeparator
         html = html + "          <li>" + cluster_name + lineSeparator
         fileOutputStreamXML.write(indent(level) + "<cluster name=\"" + cluster_name + "\">" + lineSeparator)
         i = i + 1 
         html = html + "            <ul>" + lineSeparator
         html = html + "              <li>Cluster Members" + lineSeparator
         html = html + "                <ul>" + lineSeparator
         
         # Process the Cluster Members for this cluster
         while i < len(scopes) and scopes[i].split(":")[0] == "cluster_member":
            # Add the Cluster Member name to the TreeView list
            html = html + "                  <li"
            if i == cluster_index + 1:
               html = html + " id=\"" + cluster_name + "_member\""
            member_name = scopes[i].split(":")[1]
            html = html + "><a href=\"#" + member_name + "_config\">" + member_name + "</a>" + lineSeparator
            fileOutputStreamXML.write(indent(level + 1) + "<member name=\"" + member_name + "\">" + lineSeparator)

            fileOutputStreamXML.write(buildServerConfigXML(level + 2, scopes[i]))
 
            # Check for configuration items for each Cluster Member and create a link if they exist
            ree_id, entries = findConfigIds("cluster_member", member_name + ":" + cluster_name, rees) 
            if ree_id:
               html = html + "                    <ul><li><a href=\"#" + ree_id + "\">REEs</a></li></ul>" + lineSeparator
               found_props = []
               for ree in entries:
                 found_props.append(rees_props[rees.index(ree)])
               fileOutputStreamXML.write(buildREEXML(level + 2, entries, found_props))

            url_id, entries = findConfigIds("cluster_member", member_name + ":" + cluster_name, urls)
            if url_id:
               html = html + "                    <ul><li><a href=\"#" + url_id + "\">URLs</a></li></ul>" + lineSeparator
               fileOutputStreamXML.write(buildURLXML(level + 2, entries))

            ds_id, entries = findConfigIds("cluster_member", member_name + ":" + cluster_name, dss)
            if ds_id:
               html = html + "                    <ul><li><a href=\"#" + ds_id + "\">Data Sources</a></li></ul>" + lineSeparator
               fileOutputStreamXML.write(buildDataSourceXML(level + 2, entries))

            mqcf_id, entries = findConfigIds("cluster_member", member_name + ":" + cluster_name, mqcfIds)
            if mqcf_id:
               html = html + "                    <ul><li><a href=\"#" + mqcf_id + "\">MQ Connection Factories</a></li></ul>" + lineSeparator
               fileOutputStreamXML.write(buildMQCFXML(level + 2, entries))

            mqqueue_id, entries = findConfigIds("cluster_member", member_name + ":" + cluster_name, mqQueues)
            if mqqueue_id:
               html = html + "                    <ul><li><a href=\"#" + mqqueue_id + "\">MQ Queues</a></li></ul>" + lineSeparator
               fileOutputStreamXML.write(buildMQQueueXML(level + 2, entries))

            j2ccf_id, entries = findConfigIds("cluster_member", member_name + ":" + cluster_name, j2cConnIds)
            if j2ccf_id:
               html = html + "                    <ul><li><a href=\"#" + j2ccf_id + "\">J2C Connection Factories</a></li></ul>" + lineSeparator
               fileOutputStreamXML.write(buildJ2CCFXML(level + 2, entries))

            j2cqueue_id, entries = findConfigIds("cluster_member", member_name + ":" + cluster_name, j2cQueues)
            if j2cqueue_id:
               html = html + "                    <ul><li><a href=\"#" + j2cqueue_id + "\">J2C Queues</a></li></ul>" + lineSeparator
               fileOutputStreamXML.write(buildJ2CQueueXML(level + 2, entries))

            actspec_id, entries = findConfigIds("cluster_member", member_name + ":" + cluster_name, actSpecs)
            if actspec_id:
               html = html + "                    <ul><li><a href=\"#" + actspec_id + "\">Activation Specs</a></li></ul>" + lineSeparator
               fileOutputStreamXML.write(buildActSpecXML(level + 2, entries))

            lib_id, entries = findConfigIds("cluster_member", member_name + ":" + cluster_name, libraries)
            if lib_id:
               html = html + "                    <ul><li><a href=\"#" + lib_id + "\">Shared Libraries</a></li></ul>" + lineSeparator
               fileOutputStreamXML.write(buildSharedLibrariesXML(level + 2, entries))

            var_id, entries = findConfigIds("cluster_member", member_name + ":" + cluster_name, variables)
            if var_id:
               html = html + "                    <ul><li><a href=\"#" + var_id + "\">Variables</a></li></ul>" + lineSeparator
               fileOutputStreamXML.write(buildVariablesXML(level + 2, entries))

            if not ree_id and not url_id and not ds_id and not lib_id and not var_id and not mqcf_id and not actspec_id and not j2ccf_id and not mqqueue_id and not j2cqueue_id:
               html = html + "</li>" + lineSeparator
            else:
               html = html + "                  </li>" + lineSeparator
               fileOutputStreamXML.write(indent(level + 1) + "</member>" + lineSeparator)

            i = i + 1
         
         # Close out the Cluster Member list
         html = html + "                </ul>" + lineSeparator
         html = html + "              </li>" + lineSeparator

         # Check for configuration items for the Cluster and create a link if they exist
         id, entries = findConfigIds("cluster", cluster_name, rees)
         if id:
            html = html + "              <li><a href=\"#" + id + "\">REEs</a></li>" + lineSeparator
            found_props = []
            for ree in entries:
               found_props.append(rees_props[rees.index(ree)])
            fileOutputStreamXML.write(buildREEXML(level + 1, entries, found_props))
            
         id, entries = findConfigIds("cluster", cluster_name, urls)
         if id:
            html = html + "              <li><a href=\"#" + id + "\">URLs</a></li>" + lineSeparator
            fileOutputStreamXML.write(buildURLXML(level + 1, entries))
            
         id, entries = findConfigIds("cluster", cluster_name, dss)
         if id:
            html = html + "              <li><a href=\"#" + id + "\">Data Sources</a></li>" + lineSeparator
            fileOutputStreamXML.write(buildDataSourceXML(level + 1, entries))
            
         id, entries = findConfigIds("cluster", cluster_name, mqcfIds)
         if id:
            html = html + "              <li><a href=\"#" + id + "\">MQ Connection Factories</a></li>" + lineSeparator
            fileOutputStreamXML.write(buildMQCFXML(level + 1, entries))
            
         id, entries = findConfigIds("cluster", cluster_name, mqQueues)
         if id:
            html = html + "              <li><a href=\"#" + id + "\">MQ Queues</a></li>" + lineSeparator
            fileOutputStreamXML.write(buildMQQueueXML(level + 1, entries))
            
         id, entries = findConfigIds("cluster", cluster_name, j2cConnIds)
         if id:
            html = html + "              <li><a href=\"#" + id + "\">J2C Connection Factories</a></li>" + lineSeparator
            fileOutputStreamXML.write(buildJ2CCFXML(level + 1, entries))
            
         id, entries = findConfigIds("cluster", cluster_name, j2cQueues)
         if id:
            html = html + "              <li><a href=\"#" + id + "\">J2C Queues</a></li>" + lineSeparator
            fileOutputStreamXML.write(buildJ2CQueueXML(level + 1, entries))
            
         id, entries = findConfigIds("cluster", cluster_name, actSpecs)
         if id:
            html = html + "              <li><a href=\"#" + id + "\">Activation Specs</a></li>" + lineSeparator
            fileOutputStreamXML.write(buildActSpecXML(level + 1, entries))
            
         id, entries = findConfigIds("cluster", cluster_name, libraries)
         if id:
            html = html + "              <li><a href=\"#" + id + "\">Shared Libraries</a></li>" + lineSeparator
            fileOutputStreamXML.write(buildSharedLibrariesXML(level + 1, entries))
            
         id, entries = findConfigIds("cluster", cluster_name, variables)
         if id:
            html = html + "              <li><a href=\"#" + id + "\">Variables</a></li>" + lineSeparator
            fileOutputStreamXML.write(buildVariablesXML(level + 1, entries))

         # Add the applications deployed to the Cluster to the TreeView
         i = i - 1
         apps = AdminApp.list("WebSphere:cell=" + cell + ",cluster=" + cluster_name).splitlines()
         if len(apps) > 0:
            html = html + "              <li>Applications" + lineSeparator
            html = html + "                <ul>" + lineSeparator
            fileOutputStreamXML.write(indent(level + 1) + "<applications>" + lineSeparator)
            for app in apps:
               html = html + "                  <li>" + app + "</li>" + lineSeparator
               fileOutputStreamXML.write(indent(level + 2) + "<application>" + app + "</application>" + lineSeparator)
            fileOutputStreamXML.write(indent(level + 1) + "</applications>" + lineSeparator)
            html = html + "                </ul>" + lineSeparator
            html = html + "              </li>" + lineSeparator
         html = html + "            </ul>" + lineSeparator
         html = html + "          </li>" + lineSeparator
         html = html + "        </ul>" + lineSeparator
         fileOutputStreamXML.write(indent(level) + "</cluster>" + lineSeparator)
      elif type == "node":
         # Add the node name to the TreeView list
         if not node:
            level = 1
            if clusters:
               fileOutputStreamXML.write(indent(level) + "</clusters>" + lineSeparator)
            fileOutputStreamXML.write(indent(level) + "<nodes>" + lineSeparator)
            html = html + "      <li>Nodes" + lineSeparator
            html = html + "        <ul>" + lineSeparator
         node = scopes[i].split(":")[1]
         html = html + "          <li id=\"" + node + "_node\">" + node + lineSeparator
         html = html + "            <ul>" + lineSeparator
         fileOutputStreamXML.write(indent(level + 1) + "<node name=\"" + node + "\">" + lineSeparator)
         
         # Check for configuration items for the Node and create a link if they exist
         id, entries = findConfigIds("node", node, rees)
         if id:
            html = html + "              <li><a href=\"#" + id + "\">REEs</a></li>" + lineSeparator
            found_props = []
            for ree in entries:
               found_props.append(rees_props[rees.index(ree)])
            fileOutputStreamXML.write(buildREEXML(level + 2, entries, found_props))
            
         id, entries = findConfigIds("node", node, urls)
         if id:
            print "urls"
            html = html + "              <li><a href=\"#" + id + "\">URLs</a></li>" + lineSeparator
            fileOutputStreamXML.write(buildURLXML(level + 2, entries))
            
         id, entries = findConfigIds("node", node, dss)
         if id:
            html = html + "              <li><a href=\"#" + id + "\">Data Sources</a></li>" + lineSeparator
            fileOutputStreamXML.write(buildDataSourceXML(level + 2, entries))
            
         id, entries = findConfigIds("node", node, mqcfIds)
         if id:
            html = html + "              <li><a href=\"#" + id + "\">MQ Connection Factories</a></li>" + lineSeparator
            fileOutputStreamXML.write(buildMQCFXML(level + 2, entries))
            
         id, entries = findConfigIds("node", node, mqQueues)
         if id:
            html = html + "              <li><a href=\"#" + id + "\">MQ Queues</a></li>" + lineSeparator
            fileOutputStreamXML.write(buildMQQueueXML(level + 2, entries))
            
         id, entries = findConfigIds("node", node, j2cConnIds)
         if id:
            html = html + "              <li><a href=\"#" + id + "\">J2C Connection Factories</a></li>" + lineSeparator
            fileOutputStreamXML.write(buildJ2CCFXML(level + 2, entries))
            
         id, entries = findConfigIds("node", node, j2cQueues)
         if id:
            html = html + "              <li><a href=\"#" + id + "\">J2C Queues</a></li>" + lineSeparator
            fileOutputStreamXML.write(buildJ2CQueueXML(level + 2, entries))
            
         id, entries = findConfigIds("node", node, actSpecs)
         if id:
            html = html + "              <li><a href=\"#" + id + "\">Activation Specs</a></li>" + lineSeparator
            fileOutputStreamXML.write(buildActSpecXML(level + 2, entries))
            
         id, entries = findConfigIds("node", node, libraries)
         if id:
            html = html + "              <li><a href=\"#" + id + "\">Shared Libraries</a></li>" + lineSeparator
            fileOutputStreamXML.write(buildSharedLibrariesXML(level + 2, entries))
            
         id, entries = findConfigIds("node", node, variables)
         if id:
            html = html + "              <li><a href=\"#" + id + "\">Variables</a></li>" + lineSeparator
            fileOutputStreamXML.write(buildVariablesXML(level + 2, entries))

         # Process each server under the node that isn't a Cluster Member
         i = i + 1
         if i  < len(scopes) and scopes[i].split(":")[0] == "app_server":
            # Start the list
            html = html + "              <li>Servers" + lineSeparator
            html = html + "                <ul>" + lineSeparator
            fileOutputStreamXML.write(indent(level + 2) + "<appservers>" + lineSeparator)

            while i < len(scopes) and scopes[i].split(":")[0] == "app_server":
               # Show the Application Server name in the list
               app_server = scopes[i].split(",")[0].split(":")[1]
               html = html + "                  <li><a href=\"#" + node + "_" + app_server + "_config\">" + app_server + "</a>"
               fileOutputStreamXML.write(indent(level + 3) + "<appserver name=\"" + app_server + "\">" + lineSeparator)

               fileOutputStreamXML.write(buildServerConfigXML(level + 3, scopes[i]))
                              
               # Check for configuration items for the Application Server and create a link if they exist
               id, entries = findConfigIds("app_server", app_server + ":" + node, rees)
               if id:
                  html = html + "    <ul><li><a href=\"#" + id + "\">REEs</a></li></ul>" + lineSeparator
                  found_props = []
                  for ree in entries:
                     found_props.append(rees_props[rees.index(ree)])
                  fileOutputStreamXML.write(buildREEXML(level + 4, entries, found_props))

               id, entries = findConfigIds("app_server", app_server + ":" + node, urls)
               if id:
                  html = html + "    <ul><li><a href=\"#" + id + "\">URLs</a></li></ul>" + lineSeparator
                  fileOutputStreamXML.write(buildURLXML(level + 4, entries))

               id, entries = findConfigIds("app_server", app_server + ":" + node, dss)
               if id:
                  html = html + "    <ul><li><a href=\"#" + id + "\">Data Sources</a></li></ul>" + lineSeparator
                  fileOutputStreamXML.write(buildDataSourceXML(level + 4, entries))

               id, entries = findConfigIds("app_server", app_server + ":" + node, mqcfIds)
               if id:
                  html = html + "    <ul><li><a href=\"#" + id + "\">MQ Connection Factories</a></li></ul>" + lineSeparator
                  fileOutputStreamXML.write(buildMQCFXML(level + 4, entries))

               id, entries = findConfigIds("app_server", app_server + ":" + node, mqQueues)
               if id:
                  html = html + "    <ul><li><a href=\"#" + id + "\">MQ Queues</a></li></ul>" + lineSeparator
                  fileOutputStreamXML.write(buildMQQueueXML(level + 4, entries))

               id, entries = findConfigIds("app_server", app_server + ":" + node, j2cConnIds)
               if id:
                  html = html + "    <ul><li><a href=\"#" + id + "\">J2C Connection Factories</a></li></ul>" + lineSeparator
                  fileOutputStreamXML.write(buildJ2CCFXML(level + 4, entries))

               id, entries = findConfigIds("app_server", app_server + ":" + node, j2cQueues)
               if id:
                  html = html + "    <ul><li><a href=\"#" + id + "\">J2C Queues</a></li></ul>" + lineSeparator
                  fileOutputStreamXML.write(buildJ2CQueueXML(level + 4, entries))

               id, entries = findConfigIds("app_server", app_server + ":" + node, actSpecs)
               if id:
                  html = html + "    <ul><li><a href=\"#" + id + "\">Activation Specs</a></li></ul>" + lineSeparator
                  fileOutputStreamXML.write(buildActSpecXML(level + 4, entries))

               id, entries = findConfigIds("app_server", app_server + ":" + node, libraries)
               if id:
                  html = html + "    <ul><li><a href=\"#" + id + "\">Shared Libraries</a></li></ul>" + lineSeparator
                  fileOutputStreamXML.write(buildSharedLibrariesXML(level + 4, entries))

               id, entries = findConfigIds("app_server", app_server + ":" + node, variables)
               if id:
                  html = html + "    <ul><li><a href=\"#" + id + "\">Variables</a></li></ul>" + lineSeparator
                  fileOutputStreamXML.write(buildVariablesXML(level + 4, entries))

               # Add the applications deployed to the Application Server to the TreeView
               try:
                  apps = AdminApp.list("WebSphere:cell=" + cell + ",node=" + node + ",server=" + app_server).splitlines()
               except:
                  apps = []
               if len(apps) > 0:
                  fileOutputStreamXML.write(indent(level + 4) + "<applications>" + lineSeparator)
                  html = html + """
                    <ul>
                      <li>Applications
                        <ul>
"""
                  for app in apps:
                     html = html + "                          <li>" + app + "</li>" + lineSeparator
                     fileOutputStreamXML.write(indent(level + 5) + "<application>" + app + "</application>" + lineSeparator)

                  fileOutputStreamXML.write(indent(level + 4) + "</applications>" + lineSeparator)
                  html = html + """                        </ul>
                      </li>
                    </ul>
                  </li>
"""
               else:
                  html = html + "</li>" + lineSeparator

               fileOutputStreamXML.write(indent(level + 3) + "</appserver>" + lineSeparator)
               i = i + 1

            html = html + "                </ul>" + lineSeparator
            html = html + "              </li>" + lineSeparator
            fileOutputStreamXML.write(indent(level + 2) + "</appservers>" + lineSeparator)

         html = html + "            </ul>" + lineSeparator
         html = html + "          </li>" + lineSeparator

         fileOutputStreamXML.write(indent(level + 1) + "</node>" + lineSeparator)

         i = i - 1  
      elif type == "web_server":
         # Add the Web Servers to the TreeView list
         level = 1
         if node:
            html = html + "        </ul>" + lineSeparator
            fileOutputStreamXML.write(indent(level) + "</nodes>" + lineSeparator)  
            node_close = "closed"
         if not web_server:
            html = html + "      <li>Web Servers" + lineSeparator
            html = html + "        <ul>" + lineSeparator
            fileOutputStreamXML.write(indent(level) + "<webservers>" + lineSeparator)
         while i < len(scopes) and scopes[i].split(":")[0] == "web_server":
            web_server = scopes[i].split(":")[1]
            html = html + "          <li><a href=\"#" + web_server + "_config\">" + web_server + "</a></li>" +  lineSeparator
            fileOutputStreamXML.write(indent(level + 1) + "<webserver name=\"" + web_server + "\">" + lineSeparator)
            fileOutputStreamXML.write(getPortsXML(level + 2, web_server))
            fileOutputStreamXML.write(indent(level + 1) + "</webserver>" + lineSeparator)
            i = i + 1
         html = html + "        </ul>" + lineSeparator
         i = i - 1

      i = i + 1
   if web_server:
      fileOutputStreamXML.write(indent(1) + "</webservers>" + lineSeparator)
      
   if node and not node_close:
      html = html + "        </ul>" + lineSeparator
      fileOutputStreamXML.write(indent(1) + "</nodes>" + lineSeparator)

   html = html + """      </li>
    </ul>
  </li>
</ul>
"""
   fileOutputStreamXML.write("</cell>" + lineSeparator)
   fileOutputStreamXML.close()
   #print xml
   return html


def buildREEXML(level, rees, props):
   # Init variables
   xml = indent(level) + "<rees>" + lineSeparator

   # Iterate through each REE and process
   for ree in rees:
      # Get the name and the custom properties for the REE
      name = ree.split("(")[0].replace('\"', '')
      rees_props = props[rees.index(ree)]
    
      xml = xml + indent(level + 1) + "<ree name=\"" + name + "\">" + lineSeparator
      # Iterate through the custom properties for the REE and build the HTML
      for prop in rees_props:
         propname = AdminConfig.showAttribute(prop, 'name')
         propvalue = AdminConfig.showAttribute(prop, 'value')
         if not propvalue:
            # Empty value gets an HTML non-blank space
            propvalue = ""
         else:
            # Replace special character entities
            propvalue = clean(propvalue)
         if propname.find("assword") != -1 or propname.find("cryption") != -1 or propname.find("3des") != -1 or propname.find("apikey") != -1 or propname.find("apiKey") != -1 or propname.find("apikey") != -1 or propname.find("KEY") != -1:
            if propname.find(".charset") == -1 and propname.find("extra_") == -1 and propname.find("_char") == -1 and propname.find("expir") == -1:
               # Don't display passwords, or encryption/decryption keys
               propvalue = "md5 hash: " + md5.new(propvalue).hexdigest()
         xml = xml + indent(level + 2) + "<property name=\"" + propname + "\">" +  propvalue + "</property>" + lineSeparator
      xml = xml + indent(level + 1) + "</ree>" + lineSeparator
   xml = xml + indent(level) + "</rees>" + lineSeparator
   
   return xml

# Function - Build HTML to display REEs for a given scope
def buildREETable(scope, id, rees, props):
   # Init variables
   html = ""
   title = None
   
   # Iterate through each REE and process
   for ree in rees:
      # Get the name and the custom properties for the REE
      name = ree.split("(")[0].replace('\"', '')
      rees_props = props[rees.index(ree)]
      show="show"
      if rees_props:
         # Custom properties found for REE so build the HTML
         if not title:
            html = html + "  <tr><th class=\"scope\" colspan=2><a id=\"" + id + "\">" + scope + "</a></th></tr>" + lineSeparator
            title = "done"
         html = html + "  <tr>" + lineSeparator
         html = html + "    <th class=\"name\" colspan=2>" + name + lineSeparator
         html = html + "      <div class=\"top\">" + lineSeparator
         html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
         html = html + "      </div>" + lineSeparator
         html = html + "    </th>" + lineSeparator
         html = html + "  </tr>" + lineSeparator
         
         # Iterate through the custom properties for the REE and build the HTML 
         for prop in rees_props:
            propname = AdminConfig.showAttribute(prop, 'name')
            propvalue = AdminConfig.showAttribute(prop, 'value')
            if not propvalue:
               # Empty value gets an HTML non-blank space
               propvalue = "&nbsp;"
            else:
               # Replace < and > signs
               propvalue = propvalue.replace("<", "&lt;")
               propvalue = propvalue.replace(">", "&gt;")
            if propname.find("assword") != -1 or propname.find("cryption") != -1 or propname.find("3des") != -1 or propname.find("apikey") != -1 or propname.find("apiKey") != -1 or propname.find("apikey") != -1 or propname.find("KEY") != -1:
               if propname.find(".charset") == -1 and propname.find("extra_") == -1 and propname.find("_char") == -1 and propname.find("expir") == -1:
                  # Don't display passwords, or encryption/decryption keys
                  propvalue = "md5 hash: " + md5.new(propvalue).hexdigest()
            html = html + "  <tr>" + lineSeparator
            html = html + "    <td class=\"left\" data-ree-name=\"" + scope + "|" + name + "\">" + propname + "</td><td class=\"right\">" + propvalue + "</td>" + lineSeparator
            html = html + "  </tr>" + lineSeparator
   if html:
      html = html + "  <tr><td class=\"pad\" colspan=2>&nbsp;</td></tr>" + lineSeparator

   return html

# Function - Build the REE Section 
def buildREESection(scopes, rees, rees_props):
   # Build the title
   html = "<h4><a id=\"rees\"></a>Resource Environment Entries</h4>" + lineSeparator
   html = html + "<table>" + lineSeparator

   # Iterate through the scope and build the associated table entries if REEs are found
   # for the given scope
   table = ""
   for scope in scopes:
      type = scope.split(":")[0]
      name = scope.split(":")[1]

      if type == "cell":
         tag = "Cell: " + name
      elif type == "cluster":
         cluster_name = name
         tag = "Cluster: " + cluster_name
      elif type == "cluster_member":
         tag = "Cluster: " + cluster_name + " | Member: " + name 
         name = name + ":" + cluster_name
      elif type == "node":
         node = name
         tag = "Node: " + node
      elif type == "app_server":
         tag = "Node: " + node + " | Application Server: " + name.split(",")[0] 
         name = name.split(",")[0] + ":" + node
      else:
         continue      

      # Find REEs for this scope
      id, found_rees = findConfigIds(type, name, rees)
      
      # Build table if REEs found
      if id:
         found_props = []
         for ree in found_rees:
             found_props.append(rees_props[rees.index(ree)])
         table = table + buildREETable(tag, id, found_rees, found_props)

   if table == "":
      # Entries do not exist - show empty table
      html = html + "  <tr><th>None" + lineSeparator
      html = html + "      <div class=\"top\">" + lineSeparator
      html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
      html = html + "      </div>" + lineSeparator
      html = html + "    </th>" + lineSeparator
      html = html + "  </tr>" + lineSeparator
      html = html + "  <tr><td>&nbsp;</td></tr>" + lineSeparator
   else:
      html = html + table

   html = html + "</table>" + lineSeparator
   return html


# Function - Build HTML to display URLs for a given scope
def buildURLXML(level, urls):
   # Init variables
   xml = indent(level) + "<urls>" + lineSeparator

   # Iterate through URLs and build the HTML
   for url in urls:
      name = AdminConfig.showAttribute(url, 'name')
      spec = AdminConfig.showAttribute(url, 'spec')
      xml = xml + indent(level + 1) + "<url name=\"" + name + "\">" + spec + "</url>" + lineSeparator

   xml = xml + indent(level) + "</urls>" + lineSeparator  
   return xml


# Function - Build HTML to display URLs for a given scope 
def buildURLTable(scope, id, urls):
   # Init variables
   html = ""
   show = "show"
   
   # Iterate through URLs and build the HTML
   for url in urls:
      name = AdminConfig.showAttribute(url, 'name')
      spec = AdminConfig.showAttribute(url, 'spec')
      if show:
         html = html + "  <tr>" + lineSeparator
         html = html + "    <th colspan=2><a id=\"" + id + "\">" + scope + "</a>" + lineSeparator
         html = html + "      <div class=\"top\">" + lineSeparator
         html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
         html = html + "      </div>" + lineSeparator
         html = html + "    </th>" + lineSeparator
         html = html + "  </tr>" + lineSeparator
         show = None
      html = html + "  <tr>" + lineSeparator
      html = html + "    <td class=\"left\">" + name + "</td>" + lineSeparator
      html = html + "    <td class=\"right\">" + spec + "</td>" + lineSeparator
      html = html + "  </tr>" + lineSeparator
   if not show:
      html = html + "  <tr><td colspan=2>&nbsp;</td></tr>" + lineSeparator

   return html

# Function - Build the URL Section 
def buildURLSection(scopes, urls):
   # Build the title
   html = "<h4><a id=\"urls\"></a>URLs</h4>" + lineSeparator
   html = html + "<table>" + lineSeparator

   # Iterate through the scope and build the associated table entries if URLs are found
   # for the given scope
   entries = ""
   for scope in scopes:
      type = scope.split(":")[0]
      name = scope.split(":")[1]

      if type == "cell":
         tag = "Cell: " + name
      elif type == "cluster":
         cluster_name = name
         tag = "Cluster: " + cluster_name
      elif type == "cluster_member":
         tag = "Cluster: " + cluster_name + " | Member: " + name
         name = name + ":" + cluster_name
      elif type == "node":
         node = name
         tag = "Node: " + node
      elif type == "app_server":
         tag = "Node: " + node + " | Application Server: " + name.split(",")[0]
         name = name.split(",")[0] + ":" + node
      else:
         continue

      # Find URLs for this scope and build table entries if found
      id, found_urls = findConfigIds(type, name, urls)
      if id:
         entries = entries + buildURLTable(tag, id, found_urls)

   if entries:
      # Entries exist for this scope
      html = html + entries + lineSeparator
   else:
      # Entries do not exist - show empty table
      html = html + "  <tr><th>None" + lineSeparator
      html = html + "      <div class=\"top\">" + lineSeparator
      html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
      html = html + "      </div>" + lineSeparator
      html = html + "    </th>" + lineSeparator
      html = html + "  </tr>" + lineSeparator
      html = html + "  <tr><td>&nbsp;</td></tr>" + lineSeparator

   # Close out the table
   html = html + "</table>" + lineSeparator
   return html


# Function - Build the Shared Libraries XML entries
def buildSharedLibrariesXML(level, libraries):
   # Init HTML
   xml = indent(level) + "<sharedlibs>" + lineSeparator
   for library in libraries:
      xml = xml + indent(level + 1) + "<sharedlib name=\"" + library.split("(")[0].replace('\"', '') + "\">" + lineSeparator
      xml = xml + indent(level + 2) + "<classpath>" + AdminConfig.showAttribute(library, 'classPath') + "</classpath>" + lineSeparator
      xml = xml + indent(level + 1) + "</sharedlib>" + lineSeparator

   xml = xml + indent(level) + "</sharedlibs>" + lineSeparator

   # Return generated HTML
   return xml


# Function - Build the Shared Libraries table entries
def buildSharedLibrariesTable(scope, id, libraries):
   # Init HTML
   html = "  <tr><th class=\"scope\" colspan=2><a id=\"" + id + "\">" + scope + "</a></th></tr>" + lineSeparator
   
   # Iterate through the Shared Libraries and add each to the list
   for library in libraries:
      html = html + "  <tr>" + lineSeparator
      html = html + "    <th class=\"name\" colspan=2>" + library.split("(")[0].replace('\"', '') + lineSeparator
      html = html + "      <div class=\"top\">" + lineSeparator
      html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
      html = html + "      </div>" + lineSeparator
      html = html + "    </th>" + lineSeparator
      html = html + "  </tr>" + lineSeparator
      html = html + "  <tr>" + lineSeparator
      html = html + "    <td class=\"left\">Class Path</td>" + lineSeparator
      html = html + "    <td class=\"right\">" + AdminConfig.showAttribute(library, 'classPath') + "</td>" + lineSeparator
      html = html + "  </tr>" + lineSeparator
   html = html + "  <tr><td class=\"pad\" colspan=2>&nbsp;</td></tr>" + lineSeparator

   # Return generated HTML
   return html


# Function - Build the URL Section 
def buildSharedLibrariesSection(scopes, libraries):
   # Build title
   html = "<h4><a id=\"libraries\"></a>Shared Libraries</h4>" + lineSeparator
   html = html + "<table>" + lineSeparator

   # Iterate through the scope and build the associated table entries if 
   # Shared Libraries are found for the given scope   
   table = ""
   for scope in scopes:
      type = scope.split(":")[0]
      name = scope.split(":")[1]

      if type == "cell":
         tag = "Cell: " + name
      elif type == "cluster":
         cluster_name = name
         tag = "Cluster: " + cluster_name
      elif type == "cluster_member":
         tag = "Cluster: " + cluster_name + " | Member: " + name
         name = name + ":" + cluster_name
      elif type == "node":
         node = name
         tag = "Node: " + node
      elif type == "app_server":
         tag = "Node: " + node + " | Application Server: " + name.split(",")[0] 
         name = name.split(",")[0] + ":" + node
      else:
         continue     

      # Find Shared Libraries for this scope
      id, found_libraries = findConfigIds(type, name, libraries)
      
      # Generate table entries if found
      if id:
         table = table + buildSharedLibrariesTable(tag, id, found_libraries)

   # Check for table entries
   if table == "":
      # Generate empty table
      html = html + "  <tr><th>None" + lineSeparator
      html = html + "      <div class=\"top\">" + lineSeparator
      html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
      html = html + "      </div>" + lineSeparator
      html = html + "    </th>" + lineSeparator
      html = html + "  </tr>" + lineSeparator
      html = html + "  <tr><td>&nbsp;</td></tr>" + lineSeparator
   else:
      # Add entries to HTML
      html = html + table

   # Close the table
   html = html + "</table>" + lineSeparator
   return html


# Function - Build the WAS Variables XML entries
def buildVariablesXML(level, variables):
   # Init XML
   xml = indent(level) + "<variables>" + lineSeparator

   # Iterate through the WAS Variables and add each to the list
   for variable in variables:
      value = AdminConfig.showAttribute(variable, "value")
      if value:
         xml = xml + indent(level + 1) + "<variable name=\"" + AdminConfig.showAttribute(variable, "symbolicName") + "\">" + value + "</variable>" + lineSeparator

   xml = xml + indent(level) + "</variables>" + lineSeparator

   # Return generated XML
   return xml


# Function - Build the WAS Variables table entries
def buildVariablesTable(scope, id, variables):
   # Init HTML
   html = "  <tr><th class=\"scope\" colspan=2><a id=\"" + id + "\">" + scope + "</a>" + lineSeparator
   html = html + "      <div class=\"top\">" + lineSeparator
   html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
   html = html + "      </div>" + lineSeparator
   html = html + "    </th>" + lineSeparator
   html = html + "  </tr>" + lineSeparator

   # Iterate through the WAS Variables and add each to the list
   for variable in variables:
      value = AdminConfig.showAttribute(variable, "value")
      if value:
         html = html + "  <tr>" + lineSeparator
         html = html + "    <td class=\"left\">" + AdminConfig.showAttribute(variable, "symbolicName") + "</td>" + lineSeparator
         html = html + "    <td class=\"right\">" + value + "</td>" + lineSeparator
         html = html + "  </tr>" + lineSeparator
   html = html + "  <tr><td class=\"pad\" colspan=2>&nbsp;</td></tr>" + lineSeparator

   # Return generated HTML
   return html


# Function - Build the WAS Variables Section 
def buildVariablesSection(scopes, variables):
   # Build the title
   html = "<h4><a id=\"variables\"></a>Variables</h4>" + lineSeparator
   html = html + "<table>" + lineSeparator

   # Iterate through the scope and build the associated table entries if 
   # WAS Variables are found for the given scope
   table = ""
   for scope in scopes:
      type = scope.split(":")[0]
      name = scope.split(":")[1]

      if type == "cell":
         tag = "Cell: " + name
      elif type == "cluster":
         cluster_name = name
         tag = "Cluster: " + cluster_name
      elif type == "cluster_member":
         tag = "Cluster: " + cluster_name + " | Member: " + name
         name = name + ":" + cluster_name
      elif type == "node":
         node = name
         tag = "Node: " + node
      elif type == "app_server":
         tag = "Node: " + node + " | Application Server: " + name.split(",")[0]
         name = name.split(",")[0] + ":" + node
      else:
         continue

      # Find WAS Variables for this scope
      id, found_variables = findConfigIds(type, name, variables)
      
      # Generate table entries if found
      if id:
         table = table + buildVariablesTable(tag, id, found_variables)

   # Check for table entries
   if table == "":
      # Generate empty table
      html = html + "  <tr><th>None" + lineSeparator
      html = html + "      <div class=\"top\">" + lineSeparator
      html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
      html = html + "      </div>" + lineSeparator
      html = html + "    </th>" + lineSeparator
      html = html + "  </tr>" + lineSeparator
      html = html + "  <tr><td>&nbsp;</td></tr>" + lineSeparator
   else:
      # Add entries to HTML
      html = html + table

   # Close the table
   html = html + "</table>" + lineSeparator
   return html


# Function - Get JVM Properties for the given Server
def getJVMPropertiesXML(level, server):
   # Init HTML
   xml = indent(level) + "<jvmprops>" + lineSeparator

   # Get the config id for the target server
   if ":" in server:
      search = AdminConfig.getid("/Node:" + server.split(":")[1] + "/Server:" + server.split(":")[0] + "/")
   else:
      search = AdminConfig.getid("/Server:" + server + "/")

   # Get the JVM configuration ID
   serverId = AdminConfig.list('Server', search)
   jvmId =  AdminConfig.list('JavaVirtualMachine', serverId)

   # Iterate through the Properties and add them to the list
   for property in jvmProperties:
      prop = property.split(":")[0]
      desc = property.split(":")[1]
      xml = xml + indent(level + 1) + "<property description=\"" + desc + "\">" + AdminConfig.showAttribute(jvmId, prop) + "</property>" + lineSeparator

   # Return the Server ID, JVM ID, and generated xml
   xml = xml + indent(level) + "</jvmprops>" + lineSeparator
   return serverId, jvmId, xml


# Function - Get JVM Properties for the given Server
def getJVMProperties(server):
   # Init HTML
   html = "  <tr>" + lineSeparator
   html = html + "    <th class=\"name\" colspan=2>JVM Properties" + lineSeparator
   html = html + "      <div class=\"top\">" + lineSeparator
   html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
   html = html + "      </div>" + lineSeparator
   html = html + "    </th>" + lineSeparator
   html = html + "  </tr>" + lineSeparator

   # Get the config id for the target server
   if ":" in server:
      search = AdminConfig.getid("/Node:" + server.split(":")[1] + "/Server:" + server.split(":")[0] + "/")
   else:
      search = AdminConfig.getid("/Server:" + server + "/")

   # Get the JVM configuration ID
   serverId = AdminConfig.list('Server', search)
   jvmId =  AdminConfig.list('JavaVirtualMachine', serverId)

   # Iterate through the Properties and add them to the list
   for property in jvmProperties:
      prop = property.split(":")[0]
      desc = property.split(":")[1]
      html = html + "  <tr><td class=\"left\">" + desc + "</td><td>" + AdminConfig.showAttribute(jvmId, prop) + "</td></tr>" + lineSeparator

   # Return the Server ID, JVM ID, and generated HTML
   return serverId, jvmId, html


# Function - Get Ports for a given Server
def getPortsXML(level, server):
   # Init HTML
   xml = indent(level) + "<ports>" + lineSeparator

   # Set the server and node names
   if ":" in server:
      name = server.split(":")[0]
      node = server.split(":")[1]
   else:
      name = server
      node = AdminConfig.getid("/Server:" + server + "/").split("/nodes/")[1].split("/")[0]

   # Get the configuration id for the target node
   search = AdminConfig.getid("/Node:" + node + "/")

   # Get the Server Entries (in serverindex.xml) 
   entries = AdminConfig.list("ServerEntry", search).splitlines()
   
   # Find the Server Entry for the given name and list the ports
   for entry in entries:
      if entry.startswith(name + "("):
         namedEndPoints = AdminConfig.list("NamedEndPoint", entry).splitlines()
         for namedEndPoint in namedEndPoints:
            endPoint = AdminConfig.showAttribute(namedEndPoint, "endPoint" )
            xml = xml + indent(level + 1) + "<port name=\"" + AdminConfig.showAttribute(namedEndPoint, "endPointName") + "\">" + AdminConfig.showAttribute(endPoint, "port" ) + "</port>" + lineSeparator

   # Return generated HTML
   xml = xml + indent(level) + "</ports>" + lineSeparator

   return xml


# Function - Get Ports for a given Server
def getPorts(server):
   # Init HTML
   html = "  <tr>" + lineSeparator
   html = html + "    <th class=\"name\" colspan=2>Ports" + lineSeparator
   html = html + "      <div class=\"top\">" + lineSeparator
   html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
   html = html + "      </div>" + lineSeparator
   html = html + "    </th>" + lineSeparator
   html = html + "  </tr>" + lineSeparator

   # Set the server and node names
   if ":" in server:
      name = server.split(":")[0]
      node = server.split(":")[1]
   else:
      name = server
      node = AdminConfig.getid("/Server:" + server + "/").split("/nodes/")[1].split("/")[0]

   # Get the configuration id for the target node
   search = AdminConfig.getid("/Node:" + node + "/")

   # Get the Server Entries (in serverindex.html) 
   entries = AdminConfig.list("ServerEntry", search).splitlines()
   
   # Find the Server Entry for the given name and list the ports
   for entry in entries:
      if entry.startswith(name + "("):
         namedEndPoints = AdminConfig.list("NamedEndPoint", entry).splitlines()
         for namedEndPoint in namedEndPoints:
            endPoint = AdminConfig.showAttribute(namedEndPoint, "endPoint" )
            html = html + "  <tr><td class=\"left\">" + AdminConfig.showAttribute(namedEndPoint, "endPointName") + "</td><td>" + AdminConfig.showAttribute(endPoint, "port" ) + "</td></tr>" + lineSeparator

   # Return generated HTML
   return html


# Function - Get Thread Pool settings for a given Server
def getJVMThreadPoolsXML(level, serverid):
   # Init the HTML
   xml = indent(level) + "<threadpools>" + lineSeparator

   # Get the Thread Pools for this given Server
   threadPoolMgrId = AdminConfig.list('ThreadPoolManager', serverid)
   threadPoolIds = AdminConfig.list('ThreadPool', threadPoolMgrId).splitlines()
   
   # Get the Thread Pool for the Web Container
   for threadPoolId in threadPoolIds:
      tpName = AdminConfig.showAttribute(threadPoolId, 'name')
      if tpName == "WebContainer":
         for property,desc in jvmThreadPoolProperties.items():
            value = AdminConfig.showAttribute(threadPoolId, property)
            xml = xml + indent(level + 1) + "<pool name=\"" + tpName + "\">" + lineSeparator
            xml = xml + indent(level + 2) + "<value description=\""  + desc + "\">" + value + "</value>" + lineSeparator
            xml = xml + indent(level + 1) + "</pool>" + lineSeparator
            
   # Return generated xml
   xml = xml + indent(level) + "</threadpools>" + lineSeparator
   return xml


# Function - Get Thread Pool settings for a given Server
def getJVMThreadPools(serverid):
   # Init the HTML
   html = "  <tr>" + lineSeparator
   html = html + "    <th class=\"name\" colspan=2>Thread Pools" + lineSeparator
   html = html + "      <div class=\"top\">" + lineSeparator
   html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
   html = html + "      </div>" + lineSeparator
   html = html + "    </th>" + lineSeparator
   html = html + "  </tr>" + lineSeparator

   # Get the Thread Pools for this given Server
   threadPoolMgrId = AdminConfig.list('ThreadPoolManager', serverid)
   threadPoolIds = AdminConfig.list('ThreadPool', threadPoolMgrId).splitlines()
   
   # Get the Thread Pool for the Web Container
   for threadPoolId in threadPoolIds:
      tpName = AdminConfig.showAttribute(threadPoolId, 'name')
      if tpName == "WebContainer":
         for property,desc in jvmThreadPoolProperties.items():
            value = AdminConfig.showAttribute(threadPoolId, property)
            html = html + "  <tr><td class=\"left\">" + tpName + ": " + desc + "</td><td>" + value + "</td></tr>" + lineSeparator
            
   # Return generated HTML
   return html


# Function - Get Session Management settings for a given Server
def getSessionManagementXML(level, serverid):
   # Init the xml
   xml = indent(level) + "<sessionmgnt>" + lineSeparator

   # Get the Session Management settings for this server
   tuningParamsId = AdminConfig.list("TuningParams", serverid)
   
   # Iterate through Session Management settings and add them to the list
   for property,desc in tuningParamsProperties.items():
      value = AdminConfig.showAttribute(tuningParamsId, property)
      xml = xml + indent(level + 1) + "<value description=\"" + desc + "\">" + value + "</value>" + lineSeparator

   # Return generated xml
   xml = xml + indent(level) + "</sessionmgnt>" + lineSeparator
   return xml


# Function - Get Session Management settings for a given Server
def getSessionManagement(serverid):
   # Init the HTML
   html = "  <tr>" + lineSeparator
   html = html + "    <th class=\"name\" colspan=2>Session Management" + lineSeparator
   html = html + "      <div class=\"top\">" + lineSeparator
   html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
   html = html + "      </div>" + lineSeparator
   html = html + "    </th>" + lineSeparator
   html = html + "  </tr>" + lineSeparator

   # Get the Session Management settings for this server
   tuningParamsId = AdminConfig.list("TuningParams", serverid)
   
   # Iterate through Session Management settings and add them to the list
   for property,desc in tuningParamsProperties.items():
      value = AdminConfig.showAttribute(tuningParamsId, property)
      html = html + "  <tr><td class=\"left\">" + desc + "</td><td>" + value + "</td></tr>" + lineSeparator

   # Return generated HTML
   return html


# Function - Get Trace Settings for a given Server
def getTraceSettingsXML(level, serverid):
   # Generate the HTML with the Server's Trace Settings
   return indent(level) + "<trace property=\"string\">" + AdminConfig.showAttribute(AdminConfig.list('TraceService', serverid), 'startupTraceSpecification') + "</trace>" + lineSeparator


# Function - Get Trace Settings for a given Server
def getTraceSettings(serverid):
   # Generate the HTML with the Server's Trace Settings
   html = "  <tr>" + lineSeparator
   html = html + "    <th class=\"name\" colspan=2>Trace Settings" + lineSeparator
   html = html + "      <div class=\"top\">" + lineSeparator
   html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
   html = html + "      </div>" + lineSeparator
   html = html + "    </th>" + lineSeparator
   html = html + "  </tr>" + lineSeparator
   html = html + "  <tr><td class=\"left\">Trace String</td><td>" + AdminConfig.showAttribute(AdminConfig.list('TraceService', serverid), 'startupTraceSpecification') + "</td></tr>" + lineSeparator

   # Return generated HTML
   return html


# Function - Get Process Definition Environment Entries for a given Server
def getProcessDefEnvEntries(serverid):
   # Init variable
   html = ""
   
   # Retrieve the Process Definition for the Server
   proc_def = AdminConfig.list('JavaProcessDef', serverid)
   
   # Retrieve the Environment Entries
   entries = AdminConfig.showAttribute(proc_def, 'environment')[1:-1].split(") ")
   
   # Build Environment Entries table entries if they exist
   if entries[0]:
      html = "  <tr>" + lineSeparator
      html = html + "    <th class=\"name\" colspan=2>Environment Entries" + lineSeparator
      html = html + "      <div class=\"top\">" + lineSeparator
      html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
      html = html + "      </div>" + lineSeparator
      html = html + "    </th>" + lineSeparator
      html = html + "  </tr>" + lineSeparator

      # Iterate through Custom Properties and add them to the list
      for entry in entries:
         if entry.find(")") == -1:
            entry = entry + ")"

         name = entry.split("(")[0].replace('\"','')
         value = AdminConfig.showAttribute(entry, 'value')
         if not value:
            value = "&nbsp;"
         html = html + "  <tr><td class=\"left\">" + name + "</td><td>" + value + "</td></tr>" + lineSeparator

   # Return the generated HTML
   return html


# Function - Get Custom Properties for a given JVM
def getCustomPropertiesXML(level, jvmid):
   # Init variables
   xml = ""
   
   # Retrieve Custom Properties
   props = AdminConfig.showAttribute(jvmid, 'systemProperties')[1:-1].split(") ")
   
   # Build Custom Properties table entries if they exist
   if props[0]:
      xml = indent(level) + "<customprops>" + lineSeparator

      # Iterate through Custom Properties and add them to the list
      for prop in props:
         if prop.find(")") == -1:
            prop = prop + ")"

         name = prop.split("(")[0].replace('\"','')
         value = AdminConfig.showAttribute(prop, 'value')
         if not value:
            value = ""
         xml = xml + indent(level + 1) + "<property name=\"" + name + "\">" + value + "</property>" + lineSeparator

      xml = xml + indent(level) + "</customprops>" + lineSeparator
      
   # Return the generated xml
   return xml


# Function - Get Custom Properties for a given JVM
def getCustomProperties(jvmid):
   # Init variables
   html = ""
   
   # Retrieve Custom Properties
   props = AdminConfig.showAttribute(jvmid, 'systemProperties')[1:-1].split(") ")
   
   # Build Custom Properties table entries if they exist
   if props[0]:
      html = "  <tr>" + lineSeparator
      html = html + "    <th class=\"name\" colspan=2>Custom Properties" + lineSeparator
      html = html + "      <div class=\"top\">" + lineSeparator
      html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
      html = html + "      </div>" + lineSeparator
      html = html + "    </th>" + lineSeparator
      html = html + "  </tr>" + lineSeparator

      # Iterate through Custom Properties and add them to the list
      for prop in props:
         if prop.find(")") == -1:
            prop = prop + ")"

         name = prop.split("(")[0].replace('\"','')
         value = AdminConfig.showAttribute(prop, 'value')
         if not value:
            value = "&nbsp;"
         html = html + "  <tr><td class=\"left\">" + name + "</td><td>" + value + "</td></tr>" + lineSeparator
      
   # Return the generated HTML
   return html


# Function - Build Server Configuration table
def buildServerConfigXML(level, scope):
   type = scope.split(":")[0]
   name = scope.split(":")[1]
   if type == "app_server":
      name = name.split(",")[0]
      node = scope.split(":")[2]
      name = name + ":" + node
   elif type == "web_server":
      return

   # Build the title
   xml = indent(level) + "<serverconfig>" + lineSeparator

   # List JVM Properties, Custom Properties, Thread Pools, Session Management and 
   # Trace Settings for Application Server
   serverid, jvmid, jvm_xml = getJVMPropertiesXML(level + 1, name)
   xml = xml + jvm_xml
   #xml = xml + getProcessDefEnvEntries(serverid)
   xml = xml + getCustomPropertiesXML(level + 1, jvmid)
   xml = xml + getJVMThreadPoolsXML(level + 1, serverid)
   xml = xml + getSessionManagementXML(level + 1, serverid)
   xml = xml + getTraceSettingsXML(level + 1, serverid)

   # List ports for this server
   xml = xml + getPortsXML(level + 1, name)

   # Close out the table
   xml = xml + indent(level) + "</serverconfig>" + lineSeparator
   return xml


# Function - Build Server Configuration table
def buildServerConfig(scopes):
   # Build the title
   html = "<h4><a id=\"server_config\"></a>Server Configuration</h4>" + lineSeparator
   html = html + "<table>" + lineSeparator

   # Iterate through the Scopes list and generate server configuration table entries
   for scope in scopes:
      type = scope.split(":")[0]
      name = scope.split(":")[1]
      id = name
      if type == "app_server":
         name = name.split(",")[0]
         node = scope.split(":")[2]
         title = "Node: " + node + " | Application Server: " + name
         id = node + "_" + name
         name = name + ":" + node
      elif type == "cluster_member":
         title = "Cluster Member: " + name
      elif type == "web_server":
         title = "Web Server: " + name
      else:
         continue

      html = html + "  <tr><th class=\"scope\" colspan=2><a id=\"" + id + "_config\">" + title + "</a></th></tr>" + lineSeparator

      # List JVM Properties, Custom Properties, Thread Pools, Session Management and 
      # Trace Settings for Application Server
      if type != "web_server":
         serverid, jvmid, jvm_html = getJVMProperties(name)
         html = html + jvm_html
         #html = html + getProcessDefEnvEntries(serverid)
         html = html + getCustomProperties(jvmid)
         html = html + getJVMThreadPools(serverid)
         html = html + getSessionManagement(serverid)
         html = html + getTraceSettings(serverid)

      # List ports for this server
      html = html + getPorts(name)
      html = html + "  <tr><td class=\"pad\" colspan=2>&nbsp;</td></tr>" + lineSeparator

   # Close out the table
   html = html + "</table>" + lineSeparator
   return html


# Function - Get Resource Environment Entries and filter them
def getREEs():
   # Init REEs list
   rees = []
   rees_props = []
   
   # Retrieve REEs config ids
   temp_rees = AdminConfig.list('ResourceEnvironmentProvider').splitlines()

   # Iterate through config ids and filter out WCM entries and entries without
   # custom properties   
   for ree in temp_rees:
      if ree.find("WCM ") > -1:
         continue
      entries = AdminConfig.list('ResourceEnvEntry', ree).splitlines()
      if entries:
         for entry in entries:
            props = AdminConfig.list('J2EEResourceProperty', entry).splitlines()
            if props:
               rees.append("Entry: " + entry.replace('\"', ''))
               rees_props.append(props)
      else:
         props = AdminConfig.list('J2EEResourceProperty', ree).splitlines()
         if props:
            rees.append("Provider: " + ree.replace('\"', ''))
            rees_props.append(props)

   # Return list of filtered REEs
   return rees, rees_props


# Function - Find Configuration Ids for a Specific Configuration Type
def findConfigIds(type, target, configids):
   # Init variables
   temp_configids = []
   id = None
   configtype = None
   
   # Iterate through the config ids looking for config ids at a given scope type
   for configid in configids:
      # Only process specific configuration types
      if not configtype:
         source = configid.split("#")[1].split("_")[0]
         if source == "ResourceEnvironmentProvider":
            configtype = "rees"
         elif source == "ResourceEnvEntry":
            configtype = "rees"
         elif source == "URL":
            configtype = "urls"
         elif source == "DataSource":
            configtype = "dss"
         elif source == "Library":
            configtype = "libraries"
         elif source == "VariableSubstitutionEntry":
            configtype = "variables"
         elif source == "MQQueueConnectionFactory" or source == "MQConnectionFactory":
            configtype = "mqcf"
         elif source == "J2CActivationSpec":
            configtype = "actspec"
         elif source == "J2CConnectionFactory":
            configtype = "j2ccf"
         elif source == "MQQueue":
            configtype = "mqqueue"
         elif source == "J2CAdminObject":
            configtype = "j2cqueue"
         else:
            print "Unrecognized config type in findConfigIds: " + source
            break

      # Check if current configid is for the given scope type
      #    - add config id to list of config ids to return
      #    - build the id for the configuration type
      if type == "cell":
         if configid.find("cells/" + target + "|") > 0:
            id = "cell_" + configtype
            temp_configids.append(configid)
      elif type == "cluster":
         if configid.find("/clusters/" + target + "|") > 0:
            id = "cluster_" + target + "_" + configtype
            temp_configids.append(configid)
      elif type == "cluster_member":
         cluster_member = target.split(":")[0]
         cluster_name = target.split(":")[1]
         if configid.find("/servers/" + cluster_member + "|") > 0:
            id = "cluster_" + cluster_name + "_member_" + cluster_member + "_" + configtype
            temp_configids.append(configid)
      elif type == "node":
         if configid.find("/nodes/" + target + "|") > 0:
            id = "node_" + target + "_" + configtype
            temp_configids.append(configid)
      elif type == "app_server":
         server = target.split(":")[0]
         node = target.split(":")[1]
         if configid.find("/nodes/" + node + "/servers/" + server + "|") > 0:
            id = "node_" + node + "_server_" + server + "_" + configtype
            temp_configids.append(configid)

   # For Data Source config ids, filter out Derby JDBC Providers
   if temp_configids and configtype == "dss":
      ids = []
      for configid in temp_configids:
         providerType = AdminConfig.showAttribute(configid, 'providerType')
         if not providerType or providerType.find("Derby") > -1:
            continue
         else:
            ids.append(configid)
      temp_configids = ids

   # Handle condition where no config ids are found
   if len(temp_configids) == 0:
      id = None

   # Return the id for the scope type and list of config ids
   return id, temp_configids


# Function - Get the list of Data Sources
def getDataSources():
   # Init the list
   dsIds = []
   
   # Get the list of Data Sources for the cell
   dss = AdminConfig.list('DataSource').splitlines()
   
   # Iterate through the Data Source list and filter
   # Do not return EJB Timer and OTiS Data Sources
   for ds in dss:
      if not ds.startswith("DefaultEJBTimerDataSource(") and not ds.startswith("OTiSDataSource("):
         dsIds.append(ds)

   # Return the filtered list of Data Sources
   return dsIds


# Function - Get a property for a Data Source
def getDataSourceProperty(dsProps, property):
   # Init value in case not found
   value = "&nbsp;"
   
   # Iterate through properties list and return value for the property if the property
   # is found
   for dsPropId in dsProps:
      if dsPropId.startswith(property + "("):
         value = AdminConfig.showAttribute(dsPropId, "value")
         break
   # Return the value
   return value


def clean(value):
   value = value.replace("&", "&amp;")
   value = value.replace("<", "&lt;")
   value = value.replace(">", "&gt;")
   value = value.replace("'", "&apos;")
   value = value.replace('"', "&quot;")
   
   return ''.join([c for c in value if ord(c) > 31 and ord(c) < 127])
   #return value


# Function - Build Data Sources XML
def buildDataSourceXML(level, dsIds):
   xml = indent(level) + "<datasources>" + lineSeparator

   # Iterate through each Data Source for this scope and build table entries
   for dsId in dsIds:
      providerType = AdminConfig.showAttribute(dsId, 'providerType')
      if not providerType or providerType.find("Derby") > -1:
         continue
      
      xml = xml + indent(level + 1) + "<datasource name=\"" + dsId.split("(")[0].replace('\"', '') + "\">" +  lineSeparator 
      
      # List the Data Source properties
      for property,desc in dbDataSourceProperties.items():
         value = AdminConfig.showAttribute(dsId, property)
         if value:
            xml = xml + indent(level + 2) + "<property description=\"" + desc + "\">" + clean(value) + "</property>" +  lineSeparator

      # List the Data Source Resource properties
      dsProps = AdminConfig.list("J2EEResourceProperty", dsId).splitlines()

      for property,desc in dbResourceProperties.items():
         value = getDataSourceProperty(dsProps, property)
         if value:
            xml = xml + indent(level + 2) + "<property description=\"" + desc + "\">" + clean(value) + "</property>" +  lineSeparator

      # List the Connection Pool properties
      xml = xml + indent(level + 2) + "<connpool>" + lineSeparator
      connPoolId = AdminConfig.list('ConnectionPool', dsId)
      for property,desc in connPoolProperties.items():
         value = AdminConfig.showAttribute(connPoolId, property)
         if value:
            xml = xml + indent(level + 3) + "<property description=\"" + desc + "\">" + value + "</property>" +  lineSeparator
      xml = xml + indent(level + 2) + "</connpool>" + lineSeparator
      xml = xml + indent(level + 1) + "</datasource>" + lineSeparator

   # Close out the table
   xml = xml + indent(level) + "</datasources>" + lineSeparator
   return xml


# Function - Build Data Sources Section
def buildDataSourceSection(scopes, dss):
   # Generate the title and table tags
   html = "<h4><a id=\"datasources\"></a>Data Sources</h4>" + lineSeparator
   html = html + "<table>" + lineSeparator

   # Iterate through the scope and build the associated table entries if 
   # Data Sources are ound for the given scope 
   for scope in scopes:
      type = scope.split(":")[0]
      name = scope.split(":")[1]
      if type == "cell":
         title = "Cell: " + name
      elif type == "cluster":
         title = "Cluster: " + name
         cluster_name = name
      elif type == "cluster_member":
         title = "Cluster: " + cluster_name + " | Cluster Member: " + name
         name = name + ":" + cluster_name
      elif type == "node":
         node = name
         title = "Node: " + name
      elif type == "app_server":
         title = "Node: " + node + " | Application Server: " + name.split(",")[0]
         name = name.split(",")[0] + ":" + node
      else:
         continue

      # Find Data Sources for this scope and build table entries if found
      id, dsIds = findConfigIds(type, name, dss)
      if not id:
         continue

      show = "y"
      # Iterate through each Data Source for this scope and build table entries
      for dsId in dsIds:
         providerType = AdminConfig.showAttribute(dsId, 'providerType')
         if not providerType or providerType.find("Derby") > -1:
            continue
         if show:
            html = html + "  <tr><th class=\"scope\" colspan=2><a id=\"" + id + "\">" + title + "</a></th></tr>" + lineSeparator
            show = None
        
         # Build the table header
         html = html + "  <tr>" + lineSeparator
         html = html + "    <th class=\"name\" colspan=2>" + dsId.split("(")[0].replace('\"', '') + lineSeparator
         html = html + "      <div class=\"top\">" + lineSeparator
         html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
         html = html + "      </div>" + lineSeparator
         html = html + "    </th>" + lineSeparator
         html = html + "  </tr>" + lineSeparator

         # List the Data Source properties
         for property,desc in dbDataSourceProperties.items():
            value = AdminConfig.showAttribute(dsId, property)
            if value:
               html = html + "  <tr>" + lineSeparator
               html = html + "    <td class=\"left\">" + desc + "</td>" +  lineSeparator
               html = html + "    <td>" + value + "</td>" +  lineSeparator
               html = html + "  </tr>" + lineSeparator

         # List the Data Source Resource properties
         dsProps = AdminConfig.list("J2EEResourceProperty", dsId).splitlines()

         for property,desc in dbResourceProperties.items():
            value = getDataSourceProperty(dsProps, property)
            if value:
               html = html + "  <tr>" + lineSeparator
               html = html + "    <td class=\"left\">" + desc + "</td>" +  lineSeparator
               html = html + "    <td>" + value + "</td>" +  lineSeparator
               html = html + "  </tr>" + lineSeparator

         # List the Connection Pool properties
         html = html + "  <tr>" + lineSeparator
         html = html + "    <td class=\"properties\" colspan=2><b>Connection Pool</b></td>" + lineSeparator
         html = html + "  </tr>" + lineSeparator
         connPoolId = AdminConfig.list('ConnectionPool', dsId)
         for property,desc in connPoolProperties.items():
            value = AdminConfig.showAttribute(connPoolId, property)
            if value:
               html = html + "  <tr>" + lineSeparator
               html = html + "    <td class=\"left\">" + desc + "</td>" +  lineSeparator
               html = html + "    <td>" + value + "</td>" +  lineSeparator
               html = html + "  </tr>" + lineSeparator

   # Close out the table
   html = html + "</table>" + lineSeparator
   return html


# Function - Get MQ Connection Factories
def getMQCFs():
   # Retrieve MQ Queue Connection Factories
   mqqcfIds = AdminConfig.list('MQQueueConnectionFactory').splitlines()
   if not mqqcfIds:
      mqqcfIds = []

   # Retrieve MQ Connection Factories
   mqcfIds = AdminConfig.list('MQConnectionFactory').splitlines()
   if not mqcfIds:
      mqcfIds = []

   # Return concatenated list
   return mqqcfIds + mqcfIds


# Function - Get J2C Connection Factories
def getJ2CCFs():
  j2cConnIds = []

  # Retrieve J2C Connection Factories
  connIds = AdminConfig.list('J2CConnectionFactory').splitlines()
  for connId in connIds:
     if connId.split("#")[1].split("_")[0] == "J2CConnectionFactory":
        j2cConnIds.append(connId)

  # Return the J2C Connection Factories
  return j2cConnIds


# Function - Build the MQ Connection Factory Section
def buildMQCFXML(level, mqcfIds):
   # Generate the opening tag
   xml = indent(level) + "<mqcfs>" + lineSeparator

   # Iterate through each MQ Connection Factory for this scope and build table entries
   for mqcfId in mqcfIds:
      # Generate the opening tag
      xml = xml + indent(level + 1) + "<mqcf name=\"" + mqcfId.split("(")[0].replace('\"', '') + "\">" + lineSeparator

      # List the MQ Conn Factory properties
      for property,desc in mqCFProperties.items():
         value = AdminConfig.showAttribute(mqcfId, property)
         if value:
            xml = xml + indent(level + 2) + "<property description=\"" + desc + "\">" + value + "</property>" +  lineSeparator

      try:
         # List SSL Configuration if specified
         if AdminConfig.showAttribute(mqcfId, "sslType") == "SPECIFIC":
            xml = xml + indent(level + 2) + "<sslconfig>" + AdminConfig.showAttribute(mqcfId, "sslConfiguration") + "</sslconfig>" +  lineSeparator

         # List the SSL Peer Name if specified
         sslPeerName = AdminConfig.showAttribute(mqcfId, "sslPeerName")
         if sslPeerName:
            xml = xml + indent(level + 2) + "<sslpeer>" + sslPeerName + "</sslpeer>" +  lineSeparator
      except:
         pass

      # List the Connection Pool properties
      xml = xml + indent(level + 2) + "<connpool>" + lineSeparator
      connPoolId = AdminConfig.showAttribute(mqcfId, 'connectionPool')
      for property,desc in connPoolProperties.items():
         value = AdminConfig.showAttribute(connPoolId, property)
         if value:
            xml = xml + indent(level + 3) + "<property description=\"" + desc + "\">" + value + "</property>" +  lineSeparator
      xml = xml + indent(level + 2) + "</connpool>" + lineSeparator
      xml = xml + indent(level + 1) + "</mqcf>" + lineSeparator

   # Close out the table
   xml = xml + indent(level) + "</mqcfs>" + lineSeparator
   return xml


# Function - Build the MQ Connection Factory Section
def buildMQCFSection(scopes, factoryIds):
   # Generate the title and table tags
   html = "<h4><a id=\"mqcf\"></a>MQ Connection Factories</h4>" + lineSeparator
   html = html + "<table>" + lineSeparator

   # Check for MQ Conn Factory IDs
   if not factoryIds:
      html = html + "  <tr><th>None" + lineSeparator
      html = html + "      <div class=\"top\">" + lineSeparator
      html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
      html = html + "      </div>" + lineSeparator
      html = html + "    </th>" + lineSeparator
      html = html + "  </tr>" + lineSeparator
      html = html + "  <tr><td>&nbsp;</td></tr>" + lineSeparator
   else:
      # Iterate through the scope and build the associated table entries if
      # Data Sources are ound for the given scope
      for scope in scopes:
         type = scope.split(":")[0]
         name = scope.split(":")[1]
         if type == "cell":
            title = "Cell: " + name
         elif type == "cluster":
            title = "Cluster: " + name
            cluster_name = name
         elif type == "cluster_member":
            title = "Cluster: " + cluster_name + " | Cluster Member: " + name
            name = name + ":" + cluster_name
         elif type == "node":
            node = name
            title = "Node: " + name
         elif type == "app_server":
            title = "Node: " + node + " | Application Server: " + name.split(",")[0]
            name = name.split(",")[0] + ":" + node
         else:
            continue

         # Find MQ Connection Factories  for this scope and build table entries if found
         id, mqcfIds = findConfigIds(type, name, factoryIds)
         if not id:
            continue
   
         show = "y"
         # Iterate through each MQ Connection Factory for this scope and build table entries
         for mqcfId in mqcfIds:
            if show:
               html = html + "  <tr><th class=\"scope\" colspan=2><a id=\"" + id + "\">" + title + "</a></th></tr>" + lineSeparator
               show = None

            # Build the table header
            html = html + "  <tr>" + lineSeparator
            html = html + "    <th class=\"name\" colspan=2>" + mqcfId.split("(")[0].replace('\"', '') + lineSeparator
            html = html + "      <div class=\"top\">" + lineSeparator
            html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
            html = html + "      </div>" + lineSeparator
            html = html + "    </th>" + lineSeparator
            html = html + "  </tr>" + lineSeparator

            # List the MQ Conn Factory properties
            for property,desc in mqCFProperties.items():
               value = AdminConfig.showAttribute(mqcfId, property)
               if value:
                  html = html + "  <tr>" + lineSeparator
                  html = html + "    <td class=\"left\">" + desc + "</td>" +  lineSeparator
                  html = html + "    <td>" + value + "</td>" +  lineSeparator
                  html = html + "  </tr>" + lineSeparator

            try:
               # List SSL Configuration if specified
               if AdminConfig.showAttribute(mqcfId, "sslType") == "SPECIFIC":
                  html = html + "  <tr>" + lineSeparator
                  html = html + "    <td class=\"left\">SSL Configuration</td>" +  lineSeparator
                  html = html + "    <td>" + AdminConfig.showAttribute(mqcfId, "sslConfiguration") + "</td>" +  lineSeparator
                  html = html + "  </tr>" + lineSeparator

               # List the SSL Peer Name if specified
               sslPeerName = AdminConfig.showAttribute(mqcfId, "sslPeerName")
               if sslPeerName:
                  html = html + "  <tr>" + lineSeparator
                  html = html + "    <td class=\"left\">SSL Peer Name</td>" +  lineSeparator
                  html = html + "    <td>" + sslPeerName + "</td>" +  lineSeparator
                  html = html + "  </tr>" + lineSeparator
            except:
               pass

            # List the Connection Pool properties
            html = html + "  <tr>" + lineSeparator
            html = html + "    <td class=\"properties\" colspan=2><b>Connection Pool</b></td>" + lineSeparator
            html = html + "  </tr>" + lineSeparator
            connPoolId = AdminConfig.showAttribute(mqcfId, 'connectionPool')
            for property,desc in connPoolProperties.items():
               value = AdminConfig.showAttribute(connPoolId, property)
               if value:
                  html = html + "  <tr>" + lineSeparator
                  html = html + "    <td class=\"left\">" + desc + "</td>" +  lineSeparator
                  html = html + "    <td>" + value + "</td>" +  lineSeparator
                  html = html + "  </tr>" + lineSeparator

   # Close out the table
   html = html + "</table>" + lineSeparator
   return html


# Function - Build the MQ Queue XML
def buildMQQueueXML(level, queues):
   # Generate the title and table tags
   xml = indent(level) + "<mqqueues>" + lineSeparator

   # Iterate through each MQ Queue for this scope and build table entries
   for queue in queues:
      # Build the table header
      xml = xml + indent(level + 1) + "<mqqueue name=\"" + queue.split("(")[0].replace('\"', '') + "\">" + lineSeparator

      # List the MQ Queue properties
      for property,desc in mqQueueProperties.items():
         value = AdminConfig.showAttribute(queue, property)
         if value and desc != "Name":
            xml = xml + indent(level + 2) + "<property description=\""  + desc + "\">" + value + "</property>" +  lineSeparator
    
      xml = xml + indent(level + 1) + "</mqqueue>" + lineSeparator

   # Close out the table
   xml = xml + indent(level) + "</mqqueues>" + lineSeparator
   return xml


# Function - Build the MQ Queue Section
def buildMQQueueSection(scopes, mqQueues):
   # Generate the title and table tags
   html = "<h4><a id=\"mqqueue\"></a>MQ Queues</h4>" + lineSeparator
   html = html + "<table>" + lineSeparator

   # Check for MQ Queues
   if not mqQueues:
      html = html + "  <tr><th>None" + lineSeparator
      html = html + "      <div class=\"top\">" + lineSeparator
      html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
      html = html + "      </div>" + lineSeparator
      html = html + "    </th>" + lineSeparator
      html = html + "  </tr>" + lineSeparator
      html = html + "  <tr><td>&nbsp;</td></tr>" + lineSeparator
   else:
      # Iterate through the scope and build the associated table entries if
      # MQ Queues are found for the given scope
      for scope in scopes:
         type = scope.split(":")[0]
         name = scope.split(":")[1]
         if type == "cell":
            title = "Cell: " + name
         elif type == "cluster":
            title = "Cluster: " + name
            cluster_name = name
         elif type == "cluster_member":
            title = "Cluster: " + cluster_name + " | Cluster Member: " + name
            name = name + ":" + cluster_name
         elif type == "node":
            node = name
            title = "Node: " + name
         elif type == "app_server":
            title = "Node: " + node + " | Application Server: " + name.split(",")[0]
            name = name.split(",")[0] + ":" + node
         else:
            continue

         # Find J2C Connection Factories  for this scope and build table entries if found
         id, queues = findConfigIds(type, name, mqQueues)
         if not id:
            continue

         show = "y"
         # Iterate through each MQ Queue for this scope and build table entries
         for queue in queues:
            if show:
               html = html + "  <tr><th class=\"scope\" colspan=2><a id=\"" + id + "\">" + title + "</a></th></tr>" + lineSeparator
               show = None

            # Build the table header
            html = html + "  <tr>" + lineSeparator
            html = html + "    <th class=\"name\" colspan=2>" + queue.split("(")[0].replace('\"', '') + lineSeparator
            html = html + "      <div class=\"top\">" + lineSeparator
            html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
            html = html + "      </div>" + lineSeparator
            html = html + "    </th>" + lineSeparator
            html = html + "  </tr>" + lineSeparator

            # List the MQ Queue properties
            for property,desc in mqQueueProperties.items():
               value = AdminConfig.showAttribute(queue, property)
               if value and desc != "Name":
                  html = html + "  <tr>" + lineSeparator
                  html = html + "    <td class=\"left\">" + desc + "</td>" +  lineSeparator
                  html = html + "    <td>" + value + "</td>" +  lineSeparator
                  html = html + "  </tr>" + lineSeparator

   # Close out the table
   html = html + "</table>" + lineSeparator
   return html


# Function - Build the J2C Connection Factory Section
def buildJ2CCFXML(level, j2cConnIds):
   # Generate the title and table tags
   xml = indent(level) + "<j2cconns>" + lineSeparator

   # Iterate through each J2C Connection Factory for this scope and build table entries
   for j2cConnId in j2cConnIds:
      # Build the table header
      xml = xml + indent(level + 1) + "<j2cconn name=\"" + j2cConnId.split("(")[0].replace('\"', '') + "\">" + lineSeparator

      # List the J2C Conn Factory properties
      for property,desc in j2cCFProperties.items():
         value = AdminConfig.showAttribute(j2cConnId, property)
         if value:
            xml = xml + indent(level + 2) + "<property description=\"" + desc + "\">" + value + "</property>" +  lineSeparator

      # List the J2C Conn Factory Resource properties
      resProps = AdminConfig.showAttribute(AdminConfig.showAttribute(j2cConnId, 'propertySet'), 'resourceProperties')[1:-1].split()
      for propId in resProps:
         value = AdminConfig.showAttribute(propId, "value")
         property = AdminConfig.showAttribute(propId, "name")
         if j2cCFResourceProperties.get(property,"") and value:
            xml = xml + indent(level + 2) + "<property description=\"" + j2cCFResourceProperties[property] + "\">" + value + "</property>" +  lineSeparator

      # List the Connection Pool properties
      xml = xml + indent(level + 2) + "<connpool>" + lineSeparator
      connPoolId = AdminConfig.showAttribute(j2cConnId, 'connectionPool')
      for property,desc in connPoolProperties.items():
         value = AdminConfig.showAttribute(connPoolId, property)
         if value:
            xml = xml + indent(level + 3) + "<property description=\"" + desc + "\">" + value + "</property>" +  lineSeparator
      xml = xml + indent(level + 2) + "</connpool>" + lineSeparator
      xml = xml + indent(level + 1) + "</j2cconn>" + lineSeparator

   # Close out the table
   xml = xml + indent(level) + "</j2cconns>" + lineSeparator
   return xml


# Function - Build the J2C Connection Factory Section
def buildJ2CCFSection(scopes, factoryIds):
   # Generate the title and table tags
   html = "<h4><a id=\"j2cconn\"></a>J2C Connection Factories</h4>" + lineSeparator
   html = html + "<table>" + lineSeparator

   # Check for J2C Conn Factory IDs
   if not factoryIds:
      html = html + "  <tr><th>None" + lineSeparator
      html = html + "      <div class=\"top\">" + lineSeparator
      html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
      html = html + "      </div>" + lineSeparator
      html = html + "    </th>" + lineSeparator
      html = html + "  </tr>" + lineSeparator
      html = html + "  <tr><td>&nbsp;</td></tr>" + lineSeparator
   else:
      # Iterate through the scope and build the associated table entries if
      # J2C Connection Factories are found for the given scope
      for scope in scopes:
         type = scope.split(":")[0]
         name = scope.split(":")[1]
         if type == "cell":
            title = "Cell: " + name
         elif type == "cluster":
            title = "Cluster: " + name
            cluster_name = name
         elif type == "cluster_member":
            title = "Cluster: " + cluster_name + " | Cluster Member: " + name
            name = name + ":" + cluster_name
         elif type == "node":
            node = name
            title = "Node: " + name
         elif type == "app_server":
            title = "Node: " + node + " | Application Server: " + name.split(",")[0]
            name = name.split(",")[0] + ":" + node
         else:
            continue

         # Find J2C Connection Factories  for this scope and build table entries if found
         id, j2cConnIds = findConfigIds(type, name, factoryIds)
         if not id:
            continue

         show = "y"
         # Iterate through each J2C Connection Factory for this scope and build table entries
         for j2cConnId in j2cConnIds:
            if show:
               html = html + "  <tr><th class=\"scope\" colspan=2><a id=\"" + id + "\">" + title + "</a></th></tr>" + lineSeparator
               show = None

            # Build the table header
            html = html + "  <tr>" + lineSeparator
            html = html + "    <th class=\"name\" colspan=2>" + j2cConnId.split("(")[0].replace('\"', '') + lineSeparator
            html = html + "      <div class=\"top\">" + lineSeparator
            html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
            html = html + "      </div>" + lineSeparator
            html = html + "    </th>" + lineSeparator
            html = html + "  </tr>" + lineSeparator

            # List the J2C Conn Factory properties
            for property,desc in j2cCFProperties.items():
               value = AdminConfig.showAttribute(j2cConnId, property)
               if value:
                  html = html + "  <tr>" + lineSeparator
                  html = html + "    <td class=\"left\">" + desc + "</td>" +  lineSeparator
                  html = html + "    <td>" + value + "</td>" +  lineSeparator
                  html = html + "  </tr>" + lineSeparator

            # List the J2C Conn Factory Resource properties
            resProps = AdminConfig.showAttribute(AdminConfig.showAttribute(j2cConnId, 'propertySet'), 'resourceProperties')[1:-1].split()
            for propId in resProps:
               value = AdminConfig.showAttribute(propId, "value")
               property = AdminConfig.showAttribute(propId, "name")
               if j2cCFResourceProperties.get(property,"") and value:
                  html = html + "  <tr>" + lineSeparator
                  html = html + "    <td class=\"left\">" + j2cCFResourceProperties[property] + "</td>" +  lineSeparator
                  html = html + "    <td>" + value + "</td>" +  lineSeparator
                  html = html + "  </tr>" + lineSeparator

            # List the Connection Pool properties
            html = html + "  <tr>" + lineSeparator
            html = html + "    <td class=\"properties\" colspan=2><b>Connection Pool</b></td>" + lineSeparator
            html = html + "  </tr>" + lineSeparator
            connPoolId = AdminConfig.showAttribute(j2cConnId, 'connectionPool')
            for property,desc in connPoolProperties.items():
               value = AdminConfig.showAttribute(connPoolId, property)
               if value:
                  html = html + "  <tr>" + lineSeparator
                  html = html + "    <td class=\"left\">" + desc + "</td>" +  lineSeparator
                  html = html + "    <td>" + value + "</td>" +  lineSeparator
                  html = html + "  </tr>" + lineSeparator

   # Close out the table
   html = html + "</table>" + lineSeparator
   return html


# Function - Build the J2C Queue XML
def buildJ2CQueueXML(level, queues):
   # Generate the title and table tags
   xml = indent(level) + "<j2cqueues>" + lineSeparator

   # Iterate through each J2C Queue for this scope and build table entries
   for queue in queues:
      xml = xml + indent(level + 1) + "<j2cqueue name=\"" + queue.split("(")[0].replace('\"', '') + "\">" + lineSeparator

      # List the J2C Queue properties
      for property,desc in j2cQueueProperties.items():
         value = AdminConfig.showAttribute(queue, property)
         if value and desc != "Queue Name":
            xml = xml + indent(level + 2) + "<property description=\"" + desc + "\">" + value + "</property>" +  lineSeparator

      # List the J2C Queue Resource properties
      resProps = AdminConfig.showAttribute(queue, 'properties')[1:-1].split()
      for propId in resProps:
         value = AdminConfig.showAttribute(propId, "value")
         property = AdminConfig.showAttribute(propId, "name")
         if j2cQueueResourceProperties.get(property,"") and value:
            xml = xml + indent(level + 2) + "<property description=\"" + j2cQueueResourceProperties[property] + "\">" + value + "</property>" +  lineSeparator

      xml = xml + indent(level + 1) + "</j2cqueue>" + lineSeparator

   # Close out the table
   xml = xml + indent(level) + "</j2cqueues>" + lineSeparator
   return xml


# Function - Build the J2C Queue Section
def buildJ2CQueueSection(scopes, j2cQueues):
   # Generate the title and table tags
   html = "<h4><a id=\"j2cqueue\"></a>J2C Queues</h4>" + lineSeparator
   html = html + "<table>" + lineSeparator

   # Check for J2C Queues
   if not j2cQueues:
      html = html + "  <tr><th>None" + lineSeparator
      html = html + "      <div class=\"top\">" + lineSeparator
      html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
      html = html + "      </div>" + lineSeparator
      html = html + "    </th>" + lineSeparator
      html = html + "  </tr>" + lineSeparator
      html = html + "  <tr><td>&nbsp;</td></tr>" + lineSeparator
   else:
      # Iterate through the scope and build the associated table entries if
      # J2C Queues are found for the given scope
      for scope in scopes:
         type = scope.split(":")[0]
         name = scope.split(":")[1]
         if type == "cell":
            title = "Cell: " + name
         elif type == "cluster":
            title = "Cluster: " + name
            cluster_name = name
         elif type == "cluster_member":
            title = "Cluster: " + cluster_name + " | Cluster Member: " + name
            name = name + ":" + cluster_name
         elif type == "node":
            node = name
            title = "Node: " + name
         elif type == "app_server":
            title = "Node: " + node + " | Application Server: " + name.split(",")[0]
            name = name.split(",")[0] + ":" + node
         else:
            continue

         # Find J2C Queues  for this scope and build table entries if found
         id, queues = findConfigIds(type, name, j2cQueues)
         if not id:
            continue

         show = "y"
         # Iterate through each J2C Queue for this scope and build table entries
         for queue in queues:
            if show:
               html = html + "  <tr><th class=\"scope\" colspan=2><a id=\"" + id + "\">" + title + "</a></th></tr>" + lineSeparator
               show = None

            # Build the table header
            html = html + "  <tr>" + lineSeparator
            html = html + "    <th class=\"name\" colspan=2>" + queue.split("(")[0].replace('\"', '') + lineSeparator
            html = html + "      <div class=\"top\">" + lineSeparator
            html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
            html = html + "      </div>" + lineSeparator
            html = html + "    </th>" + lineSeparator
            html = html + "  </tr>" + lineSeparator

            # List the J2C Queue properties
            for property,desc in j2cQueueProperties.items():
               value = AdminConfig.showAttribute(queue, property)
               if value:
                  html = html + "  <tr>" + lineSeparator
                  html = html + "    <td class=\"left\">" + desc + "</td>" +  lineSeparator
                  html = html + "    <td>" + value + "</td>" +  lineSeparator
                  html = html + "  </tr>" + lineSeparator

            # List the J2C Queue Resource properties
            resProps = AdminConfig.showAttribute(queue, 'properties')[1:-1].split()
            for propId in resProps:
               value = AdminConfig.showAttribute(propId, "value")
               property = AdminConfig.showAttribute(propId, "name")
               if j2cQueueResourceProperties.get(property,"") and value:
                  html = html + "  <tr>" + lineSeparator
                  html = html + "    <td class=\"left\">" + j2cQueueResourceProperties[property] + "</td>" +  lineSeparator
                  html = html + "    <td>" + value + "</td>" +  lineSeparator
                  html = html + "  </tr>" + lineSeparator

   # Close out the table
   html = html + "</table>" + lineSeparator
   return html


# Function - Build the Activation Specification XML
def buildActSpecXML(level, actSpecs):
   # Generate the title and table tags
   xml = indent(level) + "<actspecs>" + lineSeparator

   # Iterate through each Activation Spec for this scope and build table entries
   for actSpec in actSpecs:
      xml = xml + indent(level + 1) + "<actspec name=\"" + actSpec.split("(")[0].replace('\"', '') + "\">" + lineSeparator

      # List the Activation Spec properties
      for property,desc in actSpecProperties.items():
         value = AdminConfig.showAttribute(actSpec, property)
         if value:
            xml = xml + indent(level + 2) + "<property description=\"" + desc + "\">" + value + "</property>" +  lineSeparator
            
      # List the Activation Spec resource properties
      resProps = AdminConfig.showAttribute(actSpec, 'resourceProperties')[1:-1].split()
      for propId in resProps:
         value = AdminConfig.showAttribute(propId, "value")
         property = AdminConfig.showAttribute(propId, "name")
         if actSpecResourceProperties.get(property,"") and value:
            xml = xml + indent(level + 2) + "<property description=\"" + actSpecResourceProperties[property] + "\">" + value + "</property>" +  lineSeparator
         elif property == "arbitraryProperties":
            props = value.split(",")
            for prop in props:
               propName = prop.split("=")[0]
               propValue = prop.split("=")[1][1:-1]
               if propName == "sslType" and propValue == "SPECIFIC":
                   propName = "SSL Configuration"
                   propValue = props[props.index(prop) + 1].split("=")[1][1:-1]
               else:
                   propName = ""
               if propName:
                   xml = xml + indent(level + 2) + "<property description=\"" + propName + "\">" + propValue + "</property>" +  lineSeparator
      xml = xml + indent(level + 1) + "</actspec>" + lineSeparator

   # Close out the table
   xml = xml + indent(level) + "</actspecs>" + lineSeparator
   return xml


# Function - Build the Activation Specification Section
def buildActSpecSection(scopes, actSpecs):
   # Generate the title and table tags
   html = "<h4><a id=\"actspecs\"></a>Activation Specifications</h4>" + lineSeparator
   html = html + "<table>" + lineSeparator

   # Check for Activation Specs
   if not actSpecs:
      html = html + "  <tr><th>None" + lineSeparator
      html = html + "      <div class=\"top\">" + lineSeparator
      html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
      html = html + "      </div>" + lineSeparator
      html = html + "    </th>" + lineSeparator
      html = html + "  </tr>" + lineSeparator
      html = html + "  <tr><td>&nbsp;</td></tr>" + lineSeparator
   else:
      # Iterate through the scope and build the associated table entries if
      # Data Sources are ound for the given scope
      for scope in scopes:
         type = scope.split(":")[0]
         name = scope.split(":")[1]
         if type == "cell":
            title = "Cell: " + name
         elif type == "cluster":
            title = "Cluster: " + name
            cluster_name = name
         elif type == "cluster_member":
            title = "Cluster: " + cluster_name + " | Cluster Member: " + name
            name = name + ":" + cluster_name
         elif type == "node":
            node = name
            title = "Node: " + name
         elif type == "app_server":
            title = "Node: " + node + " | Application Server: " + name.split(",")[0]
            name = name.split(",")[0] + ":" + node
         else:
            continue

         # Find Activation Specs for this scope and build table entries if found
         id, actSpecIds = findConfigIds(type, name, actSpecs)
         if not id:
            continue

         show = "y"
         # Iterate through each Activation Spec for this scope and build table entries
         for actSpec in actSpecIds:
            if show:
               html = html + "  <tr><th class=\"scope\" colspan=2><a id=\"" + id + "\">" + title + "</a></th></tr>" + lineSeparator
               show = None

            # Build the table header
            html = html + "  <tr>" + lineSeparator
            html = html + "    <th class=\"name\" colspan=2>" + actSpec.split("(")[0].replace('\"', '') + lineSeparator
            html = html + "      <div class=\"top\">" + lineSeparator
            html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
            html = html + "      </div>" + lineSeparator
            html = html + "    </th>" + lineSeparator
            html = html + "  </tr>" + lineSeparator

            # List the Activation Spec properties
            for property,desc in actSpecProperties.items():
               value = AdminConfig.showAttribute(actSpec, property)
               if value:
                  html = html + "  <tr>" + lineSeparator
                  html = html + "    <td class=\"left\">" + desc + "</td>" +  lineSeparator
                  html = html + "    <td>" + value + "</td>" +  lineSeparator
                  html = html + "  </tr>" + lineSeparator
            
            # List the Activation Spec resource properties
            resProps = AdminConfig.showAttribute(actSpec, 'resourceProperties')[1:-1].split()
            for propId in resProps:
               value = AdminConfig.showAttribute(propId, "value")
               property = AdminConfig.showAttribute(propId, "name")
               if actSpecResourceProperties.get(property,"") and value:
                  html = html + "  <tr>" + lineSeparator
                  html = html + "    <td class=\"left\">" + actSpecResourceProperties[property] + "</td>" +  lineSeparator
                  html = html + "    <td>" + value + "</td>" +  lineSeparator
                  html = html + "  </tr>" + lineSeparator
               elif property == "arbitraryProperties":
                  props = value.split(",")
                  for prop in props:
                     propName = prop.split("=")[0]
                     propValue = prop.split("=")[1][1:-1]
                     if propName == "sslType" and propValue == "SPECIFIC":
                        propName = "SSL Configuration"
                        propValue = props[props.index(prop) + 1].split("=")[1][1:-1]
                     else:
                        propName = ""
                     if propName:
                        html = html + "  <tr>" + lineSeparator
                        html = html + "    <td class=\"left\">" + propName + "</td>" +  lineSeparator
                        html = html + "    <td>" + propValue + "</td>" +  lineSeparator
                        html = html + "  </tr>" + lineSeparator

   # Close out the table
   html = html + "</table>" + lineSeparator
   return html


# Function - Build the Virtual Hosts HTML Section 
def buildVirtualHosts():
   # Generate the title and table tags
   html = "<h4><a id=\"vhosts\"></a>Virtual Hosts</h4>" + lineSeparator
   html = html + "<table>" + lineSeparator

   # Iterate through the Virtual Hosts for the environment
   vhs = AdminConfig.list('VirtualHost').splitlines()
   for vh in vhs:
      # Extract the name from the config id
      name = vh.split("(")[0].replace('\"','')
      # Don't process the admin_host and proxy_host entries
      if name != "admin_host" and name != "proxy_host":
         html = html + "  <tr>" + lineSeparator
         html = html + "    <th class=\"name\" colspan=2>" + name + lineSeparator
         html = html + "      <div class=\"top\">" + lineSeparator
         html = html + "         <a href=\"#top\">Top</a>" + lineSeparator
         html = html + "      </div>" + lineSeparator
         html = html + "    </th>" + lineSeparator
         html = html + "  </tr>" + lineSeparator

         # List all of the Host Alias entries for this Virtual Host
         aliases = AdminConfig.list('HostAlias', vh).splitlines()
         for alias in aliases:
            html = html + "  <tr>" + lineSeparator
            html = html + "    <td class=\"left\">" + AdminConfig.showAttribute(alias, 'hostname') + "</td>" +  lineSeparator
            html = html + "    <td>" + AdminConfig.showAttribute(alias, 'port') + "</td>" +  lineSeparator
            html = html + "  </tr>" + lineSeparator

   # Close out the table
   html = html + "</table>" + lineSeparator
   return html

# Function - Build the Virtual Hosts XML Section
def buildVirtualHostsXML(level):
   # Generate the opening tag 
   xml = indent(level) + "<vhosts>" + lineSeparator

   # Iterate through the Virtual Hosts for the environment
   vhs = AdminConfig.list('VirtualHost').splitlines()
   for vh in vhs:
      # Extract the name from the config id
      name = vh.split("(")[0].replace('\"','')
      # Don't process the admin_host and proxy_host entries
      if name != "admin_host" and name != "proxy_host":
         # List all of the Host Alias entries for this Virtual Host
         aliases = AdminConfig.list('HostAlias', vh).splitlines()
         xml = xml + indent(level + 1) + "<vhost name=\"" + name + "\">" + lineSeparator
         for alias in aliases:
            xml = xml + indent(level + 2) + "<port alias=\"" + AdminConfig.showAttribute(alias, 'hostname') + "\">" + AdminConfig.showAttribute(alias, 'port') + "</port>" +  lineSeparator
         xml = xml + indent(level + 1) + "</vhost>" + lineSeparator

   # Close out the table
   xml = xml + indent(level) + "</vhosts>" + lineSeparator
   return xml


#-----------------------------------------------------------------------------------------
# Main Script Logic
#-----------------------------------------------------------------------------------------

# Get the input parameters
if len(sys.argv) > 0:
   env = sys.argv[0]
   htmlfile = sys.argv[1]
   xmlfile = sys.argv[2]
   console = sys.argv[3]
else:
   print "Please provide an environment, html file name, xml file name, and console url"
   sys.exit(9)

# Build the scopes list
scopes = []
buildScopes(scopes)

# Remove the double quotes from the environment title
env = env.replace('\"', '')

# Remove the double quotes from the console url
console = console.replace('\"', '')

# Open the HTML file for writing
fileOutputStream = javaio.FileOutputStream(htmlfile)

# Open the HTML file for writing
fileOutputStreamXML = javaio.FileOutputStream(xmlfile)

# Build the HTML header
print "Building HTML Header..."
fileOutputStream.write(buildHeader(env, console, scopes))

# Get the REEs for this environment
print "Filtering REEs..."
rees, rees_props = getREEs()
#for ree in rees:
#   print ree
#   print rees_props[rees.index(ree)]

# Get the URLs for this environment
print "Querying URLs..."
urls = AdminConfig.list("URL").splitlines()

# Get the Data Sources for this environment
print "Filtering JDBC Data Sources..."
dss = getDataSources()

# Get the MQ Connection Factories for this environment
print "Querying MQ Connection Factories..."
mqcfIds = getMQCFs()

# Get MQ Queues for this enviroment
print "Querying MQ Queues..."
mqQueues = AdminConfig.list('MQQueue').splitlines()

# Get J2C Queues for this environment
print "Querying J2C Queues..."
j2cQueues = AdminConfig.list('J2CAdminObject').splitlines()

# Get J2C Connection Factories for this environment
print "Filtering J2C Connection Factories..."
j2cConnIds = getJ2CCFs()

# Get the Activation Specifications for this environment
print "Querying Activation Specifications..."
actSpecs = AdminConfig.list('J2CActivationSpec').splitlines()

# Get the Shared Libraries for this environment
print "Querying Shared Libraries..."
libraries = AdminConfig.list("Library").splitlines()

# Get the WAS Variables for this environment
print "Querying WAS Variables..."
variables = AdminConfig.list("VariableSubstitutionEntry").splitlines()

# Build the TreeView with the Scopes list, REEs, URLs, Data Sources, Shared Libraries, and
# WAS Variables retrieved
print "Building Tree View..."
fileOutputStream.write(buildTreeView(fileOutputStreamXML, env, console, scopes, rees, rees_props, urls, dss, libraries, variables, mqcfIds, actSpecs, j2cConnIds, mqQueues, j2cQueues))

# Build the Server Configuration section
print "Building Server Config Section..."
fileOutputStream.write(buildServerConfig(scopes))

# Build the Data Source section
print "Building Data Source Section..."
fileOutputStream.write(buildDataSourceSection(scopes, dss))

# Build the MQ Connection Factory section
print "Building MQ Connection Factory Section..."
fileOutputStream.write(buildMQCFSection(scopes, mqcfIds))

# Build the MQ Queue section
print "Building MQ Queue Section..."
fileOutputStream.write(buildMQQueueSection(scopes, mqQueues))

# Build the J2C Connection Factory section
print "Building J2C Connection Factory Section..."
fileOutputStream.write(buildJ2CCFSection(scopes, j2cConnIds))

# Build the J2C Queue section
print "Building J2C Queue Section..."
fileOutputStream.write(buildJ2CQueueSection(scopes, j2cQueues))

# build Activation Specification section
print "Building Activation Specification Section..."
fileOutputStream.write(buildActSpecSection(scopes, actSpecs))

# Build the REE section
print "Building REE Section..."
fileOutputStream.write(buildREESection(scopes, rees, rees_props))

# Build the URL section
print "Building URL Section..."
fileOutputStream.write(buildURLSection(scopes, urls))

# Build the Shared Libararies section
print "Building Shared Libraries Section..."
fileOutputStream.write(buildSharedLibrariesSection(scopes, libraries))

# Build the WAS Variables section
print "Building WAS Variables Section..."
fileOutputStream.write(buildVariablesSection(scopes, variables))

# Build the Virtual Hosts section
print "Building Virtual Hosts Section..."
fileOutputStream.write(buildVirtualHosts())

# Close out the HTML file
fileOutputStream.write("</body>" + lineSeparator)
fileOutputStream.write("</html>" + lineSeparator)
fileOutputStream.close()
