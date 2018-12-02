<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" version="4.01"/>

<xsl:template match="cell">
  <html>
  <head>
    <link rel="stylesheet" type="text/css" href="style.css"/>
    <link rel="stylesheet" type="text/css" href="mktree.css"/>
    <script type="text/javascript" src="mktree.js"></script>
    <title><xsl:value-of select="env" /></title>
    <script>
       function myFunction()
       {
         expandTree('cell')
       }
    </script>
  </head>
  <body onLoad="myFunction()">
  <a id="top"></a>
  <div class="update">
     <a class="home" href="./index.html">Home</a><br/>
     Updated: <xsl:value-of select="lastmod" />
  </div>
  <h3><xsl:value-of select="env" />: <a href="{console}"><xsl:value-of select="console"/></a></h3>
  <div id="navcontainer">
    <ul>
      <li><a href="#scope">Scope</a></li>
      <li><a href="#server_config">Server Configurations</a></li>
      <li><a href="#datasources">Data Sources</a></li>
      <li><a href="#mqcf">MQ Conn Factories</a></li>
      <li><a href="#mqqueue">MQ Queues</a></li>
      <li><a href="#j2cconn">J2C Conn Factories</a></li>
      <li><a href="#j2cqueue">J2C Queues</a></li>
    </ul>
    <br/>
    <ul>
      <li><a href="#actspecs">Activation Specs</a></li>
      <li><a href="#rees">REEs</a></li>
      <li><a href="#urls">URLs</a></li>
      <li><a href="#libraries">Shared Libraries</a></li>
      <li><a href="#variables">Variables</a></li>
      <li><a href="#vhosts">Virtual Hosts</a></li>
    </ul>
  </div>

  <!-- Scope Tree -->
  <h4><a id="scope"></a>Scope</h4>
  <ul class="mktree" id="cell">
     <li>Cell: <xsl:value-of select="@name" />
      <ul>
        <li><a href="#vhosts">Virtual Hosts</a></li>
        <xsl:if test="rees">
        <li><a href="#cell_rees">REEs</a></li>
        </xsl:if>
        <xsl:if test="urls">
        <li><a href="#cell_urls">URLs</a></li>
        </xsl:if>
        <xsl:if test="datasources">
        <li><a href="#cell_dss">Data Sources</a></li>
        </xsl:if>
        <xsl:if test="mqcfs">
        <li><a href="#cell_mqcfs">MQ Connection Factories</a></li>
        </xsl:if>
        <xsl:if test="mqqueues">
        <li><a href="#cell_mqqueues">MQ Queues</a></li>
        </xsl:if>
        <xsl:if test="j2cconns">
        <li><a href="#cell_j2cconns">J2C Connection Factories</a></li>
        </xsl:if>
        <xsl:if test="j2cqueues">
        <li><a href="#cell_j2cqueues">J2C Queues</a></li>
        </xsl:if>
        <xsl:if test="actspecs">
        <li><a href="#cell_actspecs">Activation Specifications</a></li>
        </xsl:if>
        <xsl:if test="sharedlibs">
        <li><a href="#cell_libraries">Shared Libraries</a></li>
        </xsl:if>
        <xsl:if test="variables">
        <li><a href="#cell_variables">Variables</a></li>
        </xsl:if>
        <xsl:if test="clusters">
        <li>Clusters
          <xsl:for-each select="clusters/cluster"> 
          <ul>
            <li><xsl:value-of select="@name" />
              <xsl:if test="member">
              <ul>
                <li>Cluster Members
                  <ul>
                    <xsl:for-each select="member">
                    <li><a href="#{@name}_config"><xsl:value-of select="@name" /></a>
                    <xsl:if test="*">
                      <ul>
                      <xsl:if test="rees">
                        <li><a href="#cluster_{../@name}_member_{@name}_rees">REEs</a></li>
                      </xsl:if>
                      <xsl:if test="rees">
                        <li><a href="#cluster_{../@name}_member_{@name}_urlss">URLs</a></li>
                      </xsl:if>
                      <xsl:if test="datasources">
                        <li><a href="#cluster_{../@name}_member_{@name}_dss">Data Sources</a></li>
                      </xsl:if>
                      <xsl:if test="mqcfs">
                        <li><a href="#cluster_{../@name}_member_{@name}_mqcfs">MQ Connection Factories</a></li>
                      </xsl:if>
                      <xsl:if test="mqqueues">
                        <li><a href="#cluster_{../@name}_member_{@name}_mqqueues">MQ Queues</a></li>
                      </xsl:if>
                      <xsl:if test="j2cconns">
                        <li><a href="#cluster_{../@name}_member_{@name}_j2cconns">J2C Connection Factories</a></li>
                      </xsl:if>
                      <xsl:if test="j2cqueues">
                        <li><a href="#cluster_{../@name}_member_{@name}_j2cqueues">J2C Queues</a></li>
                      </xsl:if>
                      <xsl:if test="actspecs">
                        <li><a href="#cluster_{../@name}_member_{@name}_actspecs">Activation Specifications</a></li>
                      </xsl:if>
                      <xsl:if test="sharedlibs">
                        <li><a href="#cluster_{../@name}_member_{@name}_libraries">Shared Libraries</a></li>
                      </xsl:if>
                      <xsl:if test="variables">
                        <li><a href="#cluster_{../@name}_member_{@name}_variables">Variables</a></li>
                      </xsl:if>
                      </ul>
                    </xsl:if>
                    </li>
                    </xsl:for-each>
                  </ul>
                </li>
                <xsl:if test="rees">
                <li><a href="#cluster_{@name}_rees">REEs</a></li>
                </xsl:if>
                <xsl:if test="urls">
                <li><a href="#cluster_{@name}_urls">URLs</a></li>
                </xsl:if>
                <xsl:if test="datasources">
                <li><a href="#cluster_{@name}_dss">Data Sources</a></li>
                </xsl:if>
                <xsl:if test="mqcfs">
                <li><a href="#cluster_{@name}_mqcfs">MQ Connection Factories</a></li>
                </xsl:if>
                <xsl:if test="mqqueues">
                <li><a href="#cluster_{@name}_mqqueues">MQ Queues</a></li>
                </xsl:if>
                <xsl:if test="j2cconns">
                <li><a href="#cluster_{@name}_j2cconns">J2C Connection Factories</a></li>
                </xsl:if>
                <xsl:if test="j2cqueues">
                <li><a href="#cluster_{@name}_j2cqueues">J2C Queues</a></li>
                </xsl:if>
                <xsl:if test="actspecs">
                <li><a href="#cluster_{@name}_actspecs">Activation Specifications</a></li>
                </xsl:if>
                <xsl:if test="sharedlibs">
                <li><a href="#cluster_{@name}_libraries">Shared Libraries</a></li>
                </xsl:if>
                <xsl:if test="variables">
                  <li><a href="#cluster_{@name}_variables">Variables</a></li>
                </xsl:if>
                <xsl:if test="applications">
                <li>Applications
                  <ul>
                    <xsl:for-each select="applications/application">
                    <li><xsl:value-of select="." /></li>
                    </xsl:for-each>              
                  </ul>
                </li>
                </xsl:if>            
              </ul>
              </xsl:if>
            </li>
          </ul>
          </xsl:for-each>
        </li>
        </xsl:if>
        <xsl:if test="nodes">
        <li>Nodes
          <ul>
            <xsl:for-each select="nodes/node">
            <li id="{@name}_node"><xsl:value-of select="@name" />
            <xsl:if test="*">
              <ul>
                <xsl:if test="rees">
                <li><a href="#node{@name}_rees">REEs</a></li>
                </xsl:if>
                <xsl:if test="urls">
                <li><a href="#node_{@name}_urls">URLs</a></li>
                </xsl:if>  
                <xsl:if test="datasources">
                <li><a href="#node_{@name}_dss">Data Sources</a></li>
                </xsl:if>  
                <xsl:if test="mqcfs">
                <li><a href="#node_{@name}_mqcfs">MQ Connection Factories</a></li>
                </xsl:if>  
                <xsl:if test="mqqueues">
                <li><a href="#node_{@name}_mqqueues">MQ Queues</a></li>
                </xsl:if>  
                <xsl:if test="j2cconns">
                <li><a href="#node_{@name}_j2cconns">J2C Connection Factories</a></li>
                </xsl:if>  
                <xsl:if test="j2cqueues">
                <li><a href="#node_{@name}_j2cqueues">J2C Queues</a></li>
                </xsl:if>  
                <xsl:if test="actspecs">
                <li><a href="#node_{@name}_actspecs">Activation Specifications</a></li>
                </xsl:if>  
                <xsl:if test="sharedlibs">
                <li><a href="#node_{@name}_libraries">Shared Libraries</a></li>
                </xsl:if>  
                <xsl:if test="variables">
                <li><a href="#node_{@name}_variables">Variables</a></li>
                </xsl:if>
                <xsl:if test="appservers">
                <li>Servers
                  <ul>
                  <xsl:for-each select="appservers/appserver">
                    <li><a href="#{../../@name}_{@name}_config"><xsl:value-of select="@name" /></a>
                    <xsl:if test="*">
                      <ul>
                      <xsl:if test="rees">
                        <li><a href="#node_{../../@name}_server_{@name}_rees">REEs</a></li>
                      </xsl:if>  
                      <xsl:if test="urls">
                        <li><a href="#node_{../../@name}_server_{@name}_urls">URLs</a></li>
                      </xsl:if>  
                      <xsl:if test="datasources">
                        <li><a href="#node_{../../@name}_server_{@name}_dss">Data Sources</a></li>
                      </xsl:if>  
                      <xsl:if test="mqcfs">
                        <li><a href="#node_{../../@name}_server_{@name}_mqcfs">MQ Connection Factories</a></li>
                      </xsl:if>  
                      <xsl:if test="mqqueues">
                        <li><a href="#node_{../../@name}_server_{@name}_mqqueues">MQ Queues</a></li>
                      </xsl:if>  
                      <xsl:if test="j2cconns">
                        <li><a href="#node_{../../@name}_server_{@name}_j2cconns">J2C Connection Factories</a></li>
                      </xsl:if>  
                      <xsl:if test="j2cqueues">
                        <li><a href="#node_{../../@name}_server_{@name}_j2cqueues">J2C Queues</a></li>
                      </xsl:if>  
                      <xsl:if test="actspecs">
                        <li><a href="#node_{../../@name}_server_{@name}_actspecs">Activation Specifications</a></li>
                      </xsl:if>  
                      <xsl:if test="sharedlibs">
                        <li><a href="#node_{../../@name}_server_{@name}_libraries">Shared Libraries</a></li>
                      </xsl:if>  
                      <xsl:if test="variables">
                        <li><a href="#node_{../../@name}_server_{@name}_variables">Variables</a></li>
                      </xsl:if>
                      <xsl:if test="applications">
                        <li>Applications
                          <ul>
                          <xsl:for-each select="applications/application">
                            <li><xsl:value-of select="." /></li>
                          </xsl:for-each>              
                          </ul>
                        </li>
                      </xsl:if>                      
                      </ul>
                    </xsl:if>                      
                    </li>
                  </xsl:for-each>
                  </ul>
                </li>
                </xsl:if>
              </ul>
            </xsl:if>
            </li>
            </xsl:for-each>          
          </ul>
        </li>
        </xsl:if>
        <xsl:if test="webservers">
        <li>Web Servers
          <ul>
          <xsl:for-each select="webservers/webserver">
            <li><a href="#{@name}_config"><xsl:value-of select="@name" /></a></li>
          </xsl:for-each>
          </ul>
        </li>
        </xsl:if>
      </ul>
    </li>
  </ul>

  <!-- Server Configuration -->
  <h4><a id="server_config"></a>Server Configuration</h4>
  <table>
    <xsl:apply-templates select="clusters/cluster/member" /> 
    <xsl:apply-templates select="nodes/node/appservers/appserver" /> 
    <xsl:apply-templates select="webservers/webserver" /> 
  </table>

  <!-- Data Sources -->
  <h4><a id="datasources"></a>Data Sources</h4>
  <table>
    <xsl:apply-templates select=".//datasources" /> 
    <xsl:if test="not(.//datasources)">
    <tr><th>None
      <div class="top">
         <a href="#top">Top</a>
      </div>
    </th>
    </tr>
    <tr><td>&#160;</td></tr>
    </xsl:if>
  </table>
  
  <!-- MQ Connection Factories -->
  <h4><a id="mqcf"></a>MQ Connection Factories</h4>
  <table>
    <xsl:apply-templates select=".//mqcfs" /> 
    <xsl:if test="not(.//mqcfs)">
    <tr><th>None
      <div class="top">
         <a href="#top">Top</a>
      </div>
    </th>
    </tr>
    <tr><td>&#160;</td></tr>
    </xsl:if>
  </table>

  <!-- MQ Queues -->
  <h4><a id="mqqueue"></a>MQ Queues</h4>
  <table>
    <xsl:apply-templates select=".//mqqueues" /> 
    <xsl:if test="not(.//mqqueues)">
    <tr><th>None
      <div class="top">
         <a href="#top">Top</a>
      </div>
    </th>
    </tr>
    <tr><td>&#160;</td></tr>
    </xsl:if>
  </table>

  <!-- J2C Connection Factories -->
  <h4><a id="j2cconn"></a>J2C Connection Factories</h4>
  <table>
    <xsl:apply-templates select=".//j2cconns" /> 
    <xsl:if test="not(.//j2cconns)">
    <tr><th>None
      <div class="top">
         <a href="#top">Top</a>
      </div>
    </th>
    </tr>
    <tr><td>&#160;</td></tr>
    </xsl:if>
  </table>

  <!-- J2C Queues -->
  <h4><a id="j2cqueue"></a>J2C Queues</h4>
  <table>
    <xsl:apply-templates select=".//j2cqueues" /> 
    <xsl:if test="not(.//j2cqueues)">
    <tr><th>None
      <div class="top">
         <a href="#top">Top</a>
      </div>
    </th>
    </tr>
    <tr><td>&#160;</td></tr>
    </xsl:if>
  </table>

  <!-- Activation Specifications -->
  <h4><a id="actspecs"></a>Activation Specifications</h4>
  <table>
    <xsl:apply-templates select=".//actspecs" /> 
    <xsl:if test="not(.//actspecs)">
    <tr><th>None
      <div class="top">
         <a href="#top">Top</a>
      </div>
    </th>
    </tr>
    <tr><td>&#160;</td></tr>
    </xsl:if>
  </table>

  <!-- Resource Environment Entries (REEs) -->
  <h4><a id="rees"></a>Resource Environment Entries</h4>
  <table>
    <xsl:apply-templates select=".//rees" /> 
    <xsl:if test="not(.//rees)">
    <tr><th>None
      <div class="top">
         <a href="#top">Top</a>
      </div>
    </th>
    </tr>
    <tr><td>&#160;</td></tr>
    </xsl:if>
  </table>

  <!-- URLs -->
  <h4><a id="urls"></a>URLs</h4>
  <table>
    <xsl:apply-templates select=".//urls" /> 
    <xsl:if test="not(.//urls)">
    <tr><th>None
      <div class="top">
         <a href="#top">Top</a>
      </div>
    </th>
    </tr>
    <tr><td>&#160;</td></tr>
    </xsl:if>
  </table>

  <!-- Shared Libraries -->
  <h4><a id="libraries"></a>Shared Libraries</h4>
  <table>
    <xsl:apply-templates select=".//sharedlibs" /> 
    <xsl:if test="not(.//sharedlibs)">
    <tr><th>None
      <div class="top">
         <a href="#top">Top</a>
      </div>
    </th>
    </tr>
    <tr><td>&#160;</td></tr>
    </xsl:if>
  </table>

  <!-- Variables -->
  <h4><a id="variables"></a>Variables</h4>
  <table>
    <xsl:apply-templates select=".//variables" /> 
    <xsl:if test="not(.//variables)">
    <tr><th>None
      <div class="top">
         <a href="#top">Top</a>
      </div>
    </th>
    </tr>
    <tr><td>&#160;</td></tr>
    </xsl:if>
  </table>
  
  <!-- Virtual Hosts -->
  <h4><a id="vhosts"></a>Virtual Hosts</h4>
  <table>
    <xsl:apply-templates select="vhosts/vhost" /> 
  </table>

  </body>
  </html>
</xsl:template>

<!-- Server Configuration  -->
<xsl:template match="member">
    <tr><th class="scope" colspan="2"><a id="{@name}_config">Cluster: <xsl:value-of select="../@name" /> | Member: <xsl:value-of select="@name" /></a></th></tr>
    <xsl:apply-templates select="serverconfig" />
</xsl:template>

<xsl:template match="appserver">
    <tr><th class="scope" colspan="2"><a id="{../../@name}_{@name}_config">
    Node: <xsl:value-of select="../../@name" /> | Application Server: <xsl:value-of select="@name" /></a></th></tr>
    <xsl:apply-templates select="serverconfig" />
</xsl:template>

<xsl:template match="webserver">
    <tr><th class="scope" colspan="2"><a id="{@name}_config">Web Server: <xsl:value-of select="@name" /></a></th></tr>
    <xsl:for-each select="ports/port">
    <tr><td class="left"><xsl:value-of select="@name" /></td><td><xsl:value-of select="."/></td></tr>
    </xsl:for-each>
    <tr><td class="pad" colspan="2">&#160;</td></tr>
</xsl:template>

<xsl:template match="serverconfig">
    <tr>
      <th class="name" colspan="2">JVM Properties
        <div class="top">
          <a href="#top">Top</a>
        </div>
      </th>
    </tr>
    <xsl:apply-templates select="jvmprops/property" />
    <tr>
      <th class="name" colspan="2">Custom Properties
        <div class="top">
          <a href="#top">Top</a>
        </div>
      </th>
    </tr>
    <xsl:apply-templates select="customprops/property" />
    <tr>
      <th class="name" colspan="2">Thread Pools
        <div class="top">
          <a href="#top">Top</a>
        </div>
      </th>
    </tr>
    <xsl:for-each select="threadpools/pool/value">
    <tr><td class="left"><xsl:value-of select="../@name" /> - <xsl:value-of select="@description" /></td><td><xsl:value-of select="."/></td></tr>
    </xsl:for-each>
    <tr>
      <th class="name" colspan="2">Session Management
        <div class="top">
          <a href="#top">Top</a>
        </div>
      </th>
    </tr>
    <xsl:for-each select="sessionmgnt/value">
    <tr><td class="left"><xsl:value-of select="@description" /></td><td><xsl:value-of select="."/></td></tr>
    </xsl:for-each>
    <tr>
      <th class="name" colspan="2">Trace Settings
        <div class="top">
          <a href="#top">Top</a>
        </div>
      </th>
    </tr>
    <tr><td class="left">Trace String</td><td><xsl:value-of select="trace"/></td></tr>
    <tr>
      <th class="name" colspan="2">Ports
        <div class="top">
          <a href="#top">Top</a>
        </div>
      </th>
    </tr>
    <xsl:for-each select="ports/port">
    <tr><td class="left"><xsl:value-of select="@name" /></td><td><xsl:value-of select="."/></td></tr>
    </xsl:for-each>
    <tr><td class="pad" colspan="2">&#160;</td></tr>
</xsl:template>

<!-- Data Sources -->
<xsl:template match="datasources">
    <tr><th class="scope" colspan="2">
    <xsl:choose>
      <xsl:when test="name(..) = 'cell'">
        <a id="cell_dss">Cell: <xsl:value-of select="../@name"/></a>
      </xsl:when>
      <xsl:when test="name(..) = 'cluster'">
        <a id="cluster_{../@name}_dss">Cluster: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'member'">
        <a id="cluster_{../../@name}_member_{../@name}_dss">Cluster: <xsl:value-of select="../../@name" /> | Member: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'node'">
        <a id="node_{../@name}_dss">Node: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'appserver'">
        <a id="node_{../../../@name}_server_{../@name}_dss">Node: <xsl:value-of select="../../../@name" /> | Application Server: <xsl:value-of select="../@name" /></a>
      </xsl:when>
    </xsl:choose>
    </th></tr>
    <xsl:for-each select="datasource">
    <tr>
      <th class="name" colspan="2"><xsl:value-of select="@name" />
        <div class="top">
          <a href="#top">Top</a>
        </div>
      </th>
    </tr>

    <xsl:apply-templates select="property" /> 
    <tr>
      <td class="properties" colspan="2"><b>Connection Pool</b></td>
    </tr>
    <xsl:apply-templates select="connpool/property" /> 
    </xsl:for-each>
    <tr><td class="pad" colspan="2">&#160;</td></tr>    
</xsl:template>

  <!-- MQ Connection Factories -->
<xsl:template match="mqcfs">
    <tr><th class="scope" colspan="2">
    <xsl:choose>
      <xsl:when test="name(..) = 'cell'">
        <a id="cell_mqcfs">Cell: <xsl:value-of select="../@name"/></a>
      </xsl:when>
      <xsl:when test="name(..) = 'cluster'">
        <a id="cluster_{../@name}_mqcfs">Cluster: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'member'">
        <a id="cluster_{../../@name}_member_{../@name}_mqcfs">Cluster: <xsl:value-of select="../../@name" /> | Member: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'node'">
        <a id="node_{../@name}_mqcfs">Node: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'appserver'">
        <a id="node_{../../../@name}_server_{../@name}_mqcfs">Node: <xsl:value-of select="../../../@name" /> | Application Server: <xsl:value-of select="../@name" /></a>
      </xsl:when>
    </xsl:choose>
    </th></tr>
    <xsl:for-each select="mqcf">
    <tr>
      <th class="name" colspan="2"><xsl:value-of select="@name" />
        <div class="top">
          <a href="#top">Top</a>
        </div>
      </th>
    </tr>
    <xsl:apply-templates select="property" /> 
    <tr>
      <td class="properties" colspan="2"><b>Connection Pool</b></td>
    </tr>
    <xsl:apply-templates select="connpool/property" /> 
    </xsl:for-each>
    <tr><td class="pad" colspan="2">&#160;</td></tr>    
</xsl:template>

<!-- MQ Queues -->
<xsl:template match="mqqueues">
    <tr><th class="scope" colspan="2">
    <xsl:choose>
      <xsl:when test="name(..) = 'cell'">
        <a id="cell_mqqueues">Cell: <xsl:value-of select="../@name"/></a>
      </xsl:when>
      <xsl:when test="name(..) = 'cluster'">
        <a id="cluster_{../@name}_mqqueues">Cluster: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'member'">
        <a id="cluster_{../../@name}_member_{../@name}_mqqueues">Cluster: <xsl:value-of select="../../@name" /> | Member: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'node'">
        <a id="node_{../@name}_mqqueues">Node: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'appserver'">
        <a id="node_{../../../@name}_server_{../@name}_mqqueues">Node: <xsl:value-of select="../../../@name" /> | Application Server: <xsl:value-of select="../@name" /></a>
      </xsl:when>
    </xsl:choose>
    </th></tr>

    <xsl:for-each select="mqqueue">
    <tr>
      <th class="name" colspan="2"><xsl:value-of select="@name" />
        <div class="top">
          <a href="#top">Top</a>
        </div>
      </th>
    </tr>

    <xsl:apply-templates select="property" /> 
    </xsl:for-each>
    <tr><td class="pad" colspan="2">&#160;</td></tr>    
</xsl:template>

  <!-- J2C Connection Factories -->
<xsl:template match="j2cconns">
    <tr><th class="scope" colspan="2">
    <xsl:choose>
      <xsl:when test="name(..) = 'cell'">
        <a id="cell_j2cconns">Cell: <xsl:value-of select="../@name"/></a>
      </xsl:when>
      <xsl:when test="name(..) = 'cluster'">
        <a id="cluster_{../@name}_j2cconns">Cluster: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'member'">
        <a id="cluster_{../../@name}_member_{../@name}_j2cconns">Cluster: <xsl:value-of select="../../@name" /> | Member: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'node'">
        <a id="node_{../@name}_j2cconns">Node: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'appserver'">
        <a id="node_{../../../@name}_server_{../@name}_j2cconns">Node: <xsl:value-of select="../../../@name" /> | Application Server: <xsl:value-of select="../@name" /></a>
      </xsl:when>
    </xsl:choose>
    </th></tr>

    <xsl:for-each select="j2conn">
    <tr>
      <th class="name" colspan="2"><xsl:value-of select="@name" />
        <div class="top">
          <a href="#top">Top</a>
        </div>
      </th>
    </tr>

    <xsl:apply-templates select="property" /> 
    <tr>
      <td class="properties" colspan="2"><b>Connection Pool</b></td>
    </tr>
    <xsl:apply-templates select="connpool/property" /> 
    </xsl:for-each>
    <tr><td class="pad" colspan="2">&#160;</td></tr>    
</xsl:template>

<!-- J2C Queues -->
<xsl:template match="j2cqueues">
    <tr><th class="scope" colspan="2">
    <xsl:choose>
      <xsl:when test="name(..) = 'cell'">
        <a id="cell_j2cqueues">Cell: <xsl:value-of select="../@name"/></a>
      </xsl:when>
      <xsl:when test="name(..) = 'cluster'">
        <a id="cluster_{../@name}_j2cqueues">Cluster: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'member'">
        <a id="cluster_{../../@name}_member_{../@name}_j2cqueues">Cluster: <xsl:value-of select="../../@name" /> | Member: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'node'">
        <a id="node_{../@name}_j2cqueues">Node: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'appserver'">
        <a id="node_{../../../@name}_server_{../@name}_j2cqueues">Node: <xsl:value-of select="../../../@name" /> | Application Server: <xsl:value-of select="../@name" /></a>
      </xsl:when>
    </xsl:choose>
    </th></tr>

    <xsl:for-each select="j2cqueue">
    <tr>
      <th class="name" colspan="2"><xsl:value-of select="@name" />
        <div class="top">
          <a href="#top">Top</a>
        </div>
      </th>
    </tr>

    <xsl:apply-templates select="property" /> 
    </xsl:for-each>
    <tr><td class="pad" colspan="2">&#160;</td></tr>    
</xsl:template>

<!-- Activation Specifications -->
<xsl:template match="actspecs">
    <tr><th class="scope" colspan="2">
    <xsl:choose>
      <xsl:when test="name(..) = 'cell'">
        <a id="cell_actspecs">Cell: <xsl:value-of select="../@name"/></a>
      </xsl:when>
      <xsl:when test="name(..) = 'cluster'">
        <a id="cluster_{../@name}_actspecs">Cluster: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'member'">
        <a id="cluster_{../../@name}_member_{../@name}_actspecs">Cluster: <xsl:value-of select="../../@name" /> | Member: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'node'">
        <a id="node_{../@name}_actspecs">Node: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'appserver'">
        <a id="node_{../../../@name}_server_{../@name}_actspecs">Node: <xsl:value-of select="../../../@name" /> | Application Server: <xsl:value-of select="../@name" /></a>
      </xsl:when>
    </xsl:choose>
    </th></tr>

    <xsl:for-each select="actspec">
    <tr>
      <th class="name" colspan="2"><xsl:value-of select="@name" />
        <div class="top">
          <a href="#top">Top</a>
        </div>
      </th>
    </tr>

    <xsl:apply-templates select="property" /> 
    </xsl:for-each>
    <tr><td class="pad" colspan="2">&#160;</td></tr>    
</xsl:template>

<xsl:template match="property[@description]">
  <tr><td class="left"><xsl:value-of select="@description" /></td><td><xsl:value-of select="."/></td></tr>
</xsl:template>

<xsl:template match="property[@name]">
  <tr><td class="left"><xsl:value-of select="@name" /></td><td><xsl:value-of select="."/></td></tr>
</xsl:template>

<!-- Resource Environment Entries (REEs) -->
<xsl:template match="rees">
    <tr><th class="scope" colspan="2">
    <xsl:choose>
      <xsl:when test="name(..) = 'cell'">
        <a id="cell_rees">Cell: <xsl:value-of select="../@name"/></a>
      </xsl:when>
      <xsl:when test="name(..) = 'cluster'">
        <a id="cluster_{../@name}_rees">Cluster: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'member'">
        <a id="cluster_{../../@name}_member_{../@name}_rees">Cluster: <xsl:value-of select="../../@name" /> | Member: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'node'">
        <a id="node_{../@name}_rees">Node: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'appserver'">
        <a id="node_{../../../@name}_server_{../@name}_rees">Node: <xsl:value-of select="../../../@name" /> | Application Server: <xsl:value-of select="../@name" /></a>
      </xsl:when>
    </xsl:choose>
    </th></tr>

    <xsl:for-each select="ree">
    <tr>
      <th class="name" colspan="2"><xsl:value-of select="@name" />
        <div class="top">
          <a href="#top">Top</a>
        </div>
      </th>
    </tr>
    <xsl:apply-templates select="property" /> 
<!--    <xsl:for-each select="property">
    <tr><td class="left"><xsl:value-of select="@name" /></td><td><xsl:value-of select="."/></td></tr>
    </xsl:for-each> -->
    </xsl:for-each>
    <tr><td class="pad" colspan="2">&#160;</td></tr>    
</xsl:template>

  <!-- URLs -->
<xsl:template match="urls">
    <tr><th colspan="2">
    <xsl:choose>
      <xsl:when test="name(..) = 'cell'">
        <a id="cell_urls">Cell: <xsl:value-of select="../@name"/></a>
      </xsl:when>
      <xsl:when test="name(..) = 'cluster'">
        <a id="cluster_{../@name}_urls">Cluster: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'member'">
        <a id="cluster_{../../@name}_member_{../@name}_urls">Cluster: <xsl:value-of select="../../@name" /> | Member: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'node'">
        <a id="node_{../@name}_urls">Node: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'appserver'">
        <a id="node_{../../../@name}_server_{../@name}_urls">Node: <xsl:value-of select="../../../@name" /> | Application Server: <xsl:value-of select="../@name" /></a>
      </xsl:when>
    </xsl:choose>
       <div class="top">
          <a href="#top">Top</a>
        </div>
      </th>
    </tr>

    <xsl:for-each select="url">
    <tr><td class="left"><xsl:value-of select="@name" /></td><td><xsl:value-of select="."/></td></tr>
    </xsl:for-each>
    <tr><td class="pad" colspan="2">&#160;</td></tr>
</xsl:template>

<!-- Shared Libraries -->
<xsl:template match="sharedlibs">
    <tr><th class="scope" colspan="2">
    <xsl:choose>
      <xsl:when test="name(..) = 'cell'">
        <a id="cell_libraries">Cell: <xsl:value-of select="../@name"/></a>
      </xsl:when>
      <xsl:when test="name(..) = 'cluster'">
        <a id="cluster_{../@name}_libraries">Cluster: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'member'">
        <a id="cluster_{../../@name}_member_{../@name}_libraries">Cluster: <xsl:value-of select="../../@name" /> | Member: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'node'">
        <a id="node_{../@name}_libraries">Node: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'appserver'">
        <a id="node_{../../../@name}_server_{../@name}_libraries">Node: <xsl:value-of select="../../../@name" /> | Application Server: <xsl:value-of select="../@name" /></a>
      </xsl:when>
    </xsl:choose>
    </th></tr>

    <xsl:for-each select="sharedlib">
    <tr>
      <th class="name" colspan="2"><xsl:value-of select="@name" />
        <div class="top">
          <a href="#top">Top</a>
        </div>
      </th>
    </tr>
    <tr><td class="left">Class Path</td><td><xsl:value-of select="classpath"/></td></tr>
    </xsl:for-each>
    <tr><td class="pad" colspan="2">&#160;</td></tr>    
</xsl:template>

<!-- Variables -->
<xsl:template match="variables">
    <tr><th class="scope" colspan="2">
    <xsl:choose>
      <xsl:when test="name(..) = 'cell'">
        <a id="cell_variables">Cell: <xsl:value-of select="../@name"/></a>
      </xsl:when>
      <xsl:when test="name(..) = 'cluster'">
        <a id="cluster_{../@name}_variables">Cluster: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'member'">
        <a id="cluster_{../../@name}_member_{../@name}_variables">Cluster: <xsl:value-of select="../../@name" /> | Member: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'node'">
        <a id="node_{../@name}_variables">Node: <xsl:value-of select="../@name" /></a>
      </xsl:when>
      <xsl:when test="name(..) = 'appserver'">
        <a id="node_{../../../@name}_server_{../@name}_variables">Node: <xsl:value-of select="../../../@name" /> | Application Server: <xsl:value-of select="../@name" /></a>
      </xsl:when>
    </xsl:choose>
       <div class="top">
          <a href="#top">Top</a>
        </div>
      </th>
    </tr>
    
    <xsl:for-each select="variable">
    <tr><td class="left"><xsl:value-of select="@name"/></td><td><xsl:value-of select="."/></td></tr>
    </xsl:for-each>
    <tr><td class="pad" colspan="2">&#160;</td></tr>    
</xsl:template>

  <!-- Virtual Hosts -->
<xsl:template match="vhost">
  <tr>
    <th colspan="2"><xsl:value-of select="@name" />
      <div class="top">
         <a href="#top">Top</a>
      </div>
    </th>
  </tr>
  <xsl:for-each select="port">
  <tr><td class="left"><xsl:value-of select="@alias" /></td><td><xsl:value-of select="."/></td></tr>
  </xsl:for-each>
</xsl:template>

</xsl:stylesheet> 