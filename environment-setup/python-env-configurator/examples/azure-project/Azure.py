# -*- coding: utf-8 -*-
"""
Script Azure Update Manager + Security Center - VERSION FINALE
Logique correcte : Unhealthy / Unhealthy pour les recommandations
"""

from azure.identity import DefaultAzureCredential
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest
import pandas as pd
from datetime import datetime
import sys

class AzureUpdateManagerFinal:
    def __init__(self):
        """Initialise le client Azure Resource Graph."""
        try:
            self.credential = DefaultAzureCredential()
            self.resource_graph_client = ResourceGraphClient(self.credential)
        except Exception as e:
            print(f"❌ Erreur d'authentification Azure : {e}")
            print("Assurez-vous d'être connecté via Azure CLI, PowerShell ou Visual Studio Code.")
            sys.exit(1)

    def get_subscription_id(self):
        """Demande le Subscription ID à l'utilisateur."""
        print("\n" + "=".center(80, "="))
        print("🔧 Azure Update Manager + Security Center - VERSION FINALE".center(80))
        print("=".center(80, "="))
        return input("📝 Entrez votre Subscription ID: ").strip()

    def get_azure_secure_score(self, subscription_id):
        """Récupère l'Azure Secure Score."""
        print("🛡️  Récupération du Secure Score Azure...")
        
        queries = [
            f"""
            securityresources
            | where type == "microsoft.security/securescores"
            | where subscriptionId == '{subscription_id}'
            | extend currentScore = todouble(properties.score.current),
                     maxScore = todouble(properties.score.max),
                     percentage = round((todouble(properties.score.current) / todouble(properties.score.max)) * 100, 1)
            | project subscriptionId, currentScore, maxScore, percentage, displayName = properties.displayName
            """,
            f"""
            securityresources
            | where type == "microsoft.security/securescorecontrols"
            | where subscriptionId == '{subscription_id}'
            | summarize totalCurrent = sum(todouble(properties.score.current)), 
                       totalMax = sum(todouble(properties.score.max))
            | extend percentage = round((totalCurrent / totalMax) * 100, 1)
            | project currentScore = totalCurrent, maxScore = totalMax, percentage
            """
        ]
        
        for i, query in enumerate(queries):
            try:
                print(f"   - Tentative {i+1}/2...")
                request = QueryRequest(subscriptions=[subscription_id], query=query)
                response = self.resource_graph_client.resources(request)
                
                if response.data and len(response.data) > 0:
                    data = response.data[0]
                    print(f"   ✅ Secure Score récupéré: {data.get('percentage', 0)}%")
                    return data
                    
            except Exception as e:
                print(f"   ⚠️  Méthode {i+1} échouée: {e}")
                continue
        
        print("   ❌ Secure Score non disponible")
        return None

    def extract_vm_id_from_assessment(self, assessment_id):
        """Extrait l'ID de la VM depuis l'assessmentId."""
        try:
            parts = assessment_id.split('/providers/Microsoft.Security/assessments')[0]
            return parts
        except:
            return assessment_id

    def get_high_severity_machine_recommendations(self, subscription_id):
        """Récupère les recommandations avec filtre GA (comme dans le portail)."""
        print("🚨 Récupération des recommandations haute sévérité - Avec filtre GA...")
        
        query = f"""
        securityresources
        | where type == "microsoft.security/assessments"
        | where subscriptionId == '{subscription_id}'
        | where properties.metadata.severity == "High"
        | where properties.status.code == "Unhealthy"
        | where isempty(properties.metadata.preview) or properties.metadata.preview == false  // FILTRE GA
        | where properties.displayName contains "machine" or 
                properties.displayName contains "Machine" or
                properties.displayName contains "VM" or
                properties.displayName contains "virtual" or
                properties.displayName contains "server" or
                properties.displayName contains "Server" or
                properties.displayName contains "compute" or
                properties.displayName contains "Compute" or
                properties.displayName contains "updates" or
                properties.displayName contains "Updates"
        | extend recommendationName = tostring(properties.displayName),
                statusCode = tostring(properties.status.code),
                category = tostring(properties.metadata.categories[0]),
                assessmentId = id,
                preview = properties.metadata.preview
        | project recommendationName, statusCode, category, assessmentId, preview
        """
        
        try:
            request = QueryRequest(subscriptions=[subscription_id], query=query)
            response = self.resource_graph_client.resources(request)
            
            if not response.data:
                return pd.DataFrame()
            
            df = pd.DataFrame(response.data)
            print(f"   ✅ {len(df)} évaluations Unhealthy récupérées")
            
            # Extraire les VM IDs depuis les assessmentId
            df['vmId'] = df['assessmentId'].apply(self.extract_vm_id_from_assessment)
            
            results = []
            for rec_name in df['recommendationName'].unique():
                rec_data = df[df['recommendationName'] == rec_name]
                
                # Compter les VMs UNIQUES Unhealthy
                unique_unhealthy_vms = set(rec_data['vmId'])
                unhealthy_count = len(unique_unhealthy_vms)
                
                category = rec_data['category'].iloc[0]
                
                # LOGIQUE FINALE : Unhealthy / Unhealthy = "X of X"
                affected_resources = f"{unhealthy_count} of {unhealthy_count} virtual machines"
                
                results.append({
                    'recommendationName': rec_name,
                    'category': category,
                    'affectedCount': unhealthy_count,
                    'affectedResources': affected_resources
                })
            
            result_df = pd.DataFrame(results)
            result_df = result_df.sort_values('affectedCount', ascending=False)
            
            print(f"   📊 {len(result_df)} types de recommandations trouvées")
            for _, row in result_df.head(3).iterrows():
                rec_preview = row['recommendationName'][:50] + "..." if len(row['recommendationName']) > 50 else row['recommendationName']
                print(f"      - {rec_preview}: {row['affectedResources']}")
            
            return result_df
            
        except Exception as e:
            print(f"   ❌ Erreur lors de la récupération: {e}")
            return pd.DataFrame()
        
        
    def get_high_severity_azure_recommendations(self, subscription_id):
        """Récupère les recommandations haute sévérité pour Azure (Subscriptions + Storage)."""
        print("🌐 Récupération des recommandations haute sévérité Azure (Subscriptions + Storage)...")
        
        query = f"""
        securityresources
        | where type == "microsoft.security/assessments"
        | where subscriptionId == '{subscription_id}'
        | where properties.metadata.severity == "High"
        | where properties.status.code == "Unhealthy"
        | where isempty(properties.metadata.preview) or properties.metadata.preview == false
        | extend recommendationName = tostring(properties.displayName),
                statusCode = tostring(properties.status.code),
                category = tostring(properties.metadata.categories[0]),
                assessmentId = id
        | extend resourceType = case(
            assessmentId contains "/storageAccounts/", "Storage account",
            assessmentId matches regex @"^/subscriptions/[^/]+/providers/Microsoft\.Security/assessments/", "Subscription",
            "Other"
        )
        | where resourceType in ("Storage account", "Subscription")
        | project recommendationName, statusCode, category, assessmentId, resourceType
        | order by recommendationName asc
        """
        
        try:
            request = QueryRequest(subscriptions=[subscription_id], query=query)
            response = self.resource_graph_client.resources(request)
            
            if not response.data:
                return pd.DataFrame()
            
            df = pd.DataFrame(response.data)
            print(f"   ✅ {len(df)} évaluations Azure Unhealthy récupérées")
            
            results = []
            for rec_name in df['recommendationName'].unique():
                rec_data = df[df['recommendationName'] == rec_name]
                
                # Compter les assessmentId UNIQUES (au lieu des resourceId)
                unique_unhealthy_assessments = set(rec_data['assessmentId'])
                unhealthy_count = len(unique_unhealthy_assessments)
                
                category = rec_data['category'].iloc[0]
                resource_type = rec_data['resourceType'].iloc[0]
                
                # Logique : Unhealthy / Unhealthy = "X of X"
                resource_label = "subscriptions" if resource_type == "Subscription" else "storage accounts"
                affected_resources = f"{unhealthy_count} of {unhealthy_count} {resource_label}"
                
                results.append({
                    'recommendationName': rec_name,
                    'category': category,
                    'affectedCount': unhealthy_count,
                    'affectedResources': affected_resources,
                    'resourceType': resource_type
                })
            
            result_df = pd.DataFrame(results)
            result_df = result_df.sort_values('recommendationName', ascending=True)
            
            print(f"   📊 {len(result_df)} types de recommandations Azure trouvées")
            for _, row in result_df.head(3).iterrows():
                rec_preview = row['recommendationName'][:50] + "..." if len(row['recommendationName']) > 50 else row['recommendationName']
                print(f"      - {rec_preview}: {row['affectedResources']}")
            
            return result_df
            
        except Exception as e:
            print(f"   ❌ Erreur lors de la récupération des recommandations Azure: {e}")
            return pd.DataFrame()
        


    def get_all_managed_vms_complete(self, subscription_id):
        """Récupère toutes les VMs avec analyse complète des données de patch."""
        print("📋 Récupération complète des VMs et données de patch...")
        
        query = f"""
        ((resources
        | where type =~ "microsoft.compute/virtualmachines"
        | extend os = tolower(properties.storageProfile.osDisk.osType)
        | extend status = tostring(properties.extended.instanceView.powerState.displayStatus)
        | extend vmType = "Azure VM"
        | where status !in ("VM deallocated", "VM stopped", "VM stopping", "VM deallocating", "VM starting")
        | project id, joinId = tolower(id), subscriptionId, name, resourceGroup, location, os, status, vmType)
        | union (resources
        | where type =~ "microsoft.hybridcompute/machines"
        | where properties.osName in~ ('Linux','Windows') or properties.osType in~ ('Linux','Windows')
        | extend os = tolower(coalesce(properties.osName, properties.osType))
        | extend status = tostring(properties.status)
        | extend vmType = "Arc Machine"
        | where status =~ "Connected"
        | project id, joinId = tolower(id), subscriptionId, name, resourceGroup, location, os, status, vmType))
        | where subscriptionId == '{subscription_id}'
        | join kind=leftouter (
            patchassessmentresources
            | where type in~ ("microsoft.compute/virtualmachines/patchassessmentresults", "microsoft.hybridcompute/machines/patchassessmentresults")
            | parse id with resourceId "/patchAssessmentResults" *
            | extend resourceId = tolower(resourceId)
            | project resourceId, 
                      assessmentStatus = tostring(properties.status),
                      criticalCount = toint(properties.availablePatchCountByClassification.critical),
                      securityCount = toint(properties.availablePatchCountByClassification.security),
                      otherCount = toint(properties.availablePatchCountByClassification.other),
                      totalCount = toint(properties.availablePatchCount),
                      lastAssessmentTime = todatetime(properties.lastModifiedDateTime),
                      isUnsupported = (isnotnull(properties.configurationStatus.vmGuestPatchReadiness.detectedVMGuestPatchSupportState) and 
                                     (properties.configurationStatus.vmGuestPatchReadiness.detectedVMGuestPatchSupportState =~ "Unsupported")),
                      rebootPending = tobool(properties.rebootPending)
        ) on $left.joinId == $right.resourceId
        | extend hasValidPatchData = (isnotnull(resourceId) and assessmentStatus =~ "Succeeded" and isUnsupported != true)
        | extend hasPendingUpdates = (hasValidPatchData == true and (criticalCount > 0 or securityCount > 0))
        | extend criticalCount = iff(hasValidPatchData, criticalCount, 0)
        | extend securityCount = iff(hasValidPatchData, securityCount, 0)
        | extend otherCount = iff(hasValidPatchData, otherCount, 0)
        | extend totalCount = iff(hasValidPatchData, totalCount, 0)
        | extend noDataReason = case(
            isnull(resourceId), "Aucune évaluation",
            isUnsupported == true, "Image non supportée", 
            assessmentStatus != "Succeeded", strcat("Évaluation ", assessmentStatus),
            "Données disponibles"
        )
        | project name, resourceGroup, location, os, status, vmType, 
                  hasValidPatchData, hasPendingUpdates, assessmentStatus, noDataReason,
                  criticalCount, securityCount, otherCount, totalCount, lastAssessmentTime, isUnsupported, rebootPending
        | order by name asc
        """
        
        request = QueryRequest(subscriptions=[subscription_id], query=query)
        response = self.resource_graph_client.resources(request)
        
        if not response.data:
            return pd.DataFrame()
        
        return pd.DataFrame(response.data)

    def process_vm_data(self, subscription_id):
        """Traite les données des VMs."""
        try:
            print("\n🔍 Analyse des données de patch...")
            df_all_vms = self.get_all_managed_vms_complete(subscription_id)
            
            if not df_all_vms.empty:
                df_pending = df_all_vms[df_all_vms['hasPendingUpdates'] == True].copy()
                df_no_data = df_all_vms[df_all_vms['hasValidPatchData'] == False].copy()
                
                print(f"   • VMs avec mises à jour: {len(df_pending)}")
                print(f"   • VMs sans données: {len(df_no_data)}")
                
                # Standardiser les colonnes
                if not df_pending.empty:
                    df_pending = df_pending.rename(columns={
                        'name': 'vmName',
                        'os': 'osType',
                        'status': 'powerState'
                    })
                    df_pending['osType'] = df_pending['osType'].str.title()
                
                if not df_no_data.empty:
                    df_no_data = df_no_data.rename(columns={
                        'name': 'vmName',
                        'os': 'osType',
                        'status': 'powerState'
                    })
                    df_no_data['osType'] = df_no_data['osType'].str.title()
                
                return df_pending, df_no_data
            else:
                return pd.DataFrame(), pd.DataFrame()
                
        except Exception as e:
            print(f"❌ Erreur lors du traitement: {e}")
            return pd.DataFrame(), pd.DataFrame()
        
        
    

    def generate_complete_html_report(self, df_pending, df_no_data, secure_score, df_recommendations_vms, df_recommendations_azure):
        """Génère le rapport HTML complet avec recommandations Azure."""
        
        # Statistiques globales
        total_affected_vms = df_recommendations_vms['affectedCount'].sum() if not df_recommendations_vms.empty else 0
        total_affected_azure = df_recommendations_azure['affectedCount'].sum() if not df_recommendations_azure.empty else 0
        
        # Section Secure Score
        secure_score_html = ""
        if secure_score and 'percentage' in secure_score:
            score_color = "success" if secure_score['percentage'] >= 80 else "warning" if secure_score['percentage'] >= 60 else "critical"
            secure_score_html = f"""
            <div class="stat-box {score_color}">
                <h3>{secure_score['percentage']}%</h3>
                <p>Secure Score</p>
                <small>{secure_score.get('currentScore', 0):.1f} / {secure_score.get('maxScore', 0):.1f}</small>
            </div>
            """
        else:
            secure_score_html = f"""
            <div class="stat-box secondary">
                <h3>N/A</h3>
                <p>Secure Score</p>
                <small>Non disponible</small>
            </div>
            """
        
        stats_html = f"""
        <div class="stats-container">
            <div class="stat-box critical">
                <h3>{len(df_pending)}</h3>
                <p>VMs avec mises à jour</p>
                <small>Critiques + Sécurité</small>
            </div>
            <div class="stat-box warning">
                <h3>{len(df_no_data)}</h3>
                <p>VMs sans données</p>
                <small>À investiguer</small>
            </div>
            <div class="stat-box info">
                <h3>{len(df_recommendations_vms)}</h3>
                <p>Recommandations Machines</p>
                <small>{total_affected_vms} VMs concernées</small>
            </div>
            <div class="stat-box secondary">
                <h3>{len(df_recommendations_azure)}</h3>
                <p>Recommandations Azure</p>
                <small>{total_affected_azure} ressources concernées</small>
            </div>
            {secure_score_html}
        </div>
        """
        
        html_content = stats_html

        # Section Secure Score détaillée
        if secure_score and 'percentage' in secure_score:
            html_content += f"""
                <h2>🛡️ Azure Secure Score</h2>
                <div class="secure-score-detail">
                    <div class="score-info">
                        <p><strong>Score actuel :</strong> {secure_score.get('currentScore', 0):.1f} / {secure_score.get('maxScore', 0):.1f} ({secure_score['percentage']}%)</p>
                        <div class="score-bar">
                            <div class="score-progress" style="width: {secure_score['percentage']}%"></div>
                        </div>
                    </div>
                </div>
                <br>
            """

        # Section Recommandations Azure haute sévérité
        html_content += f"""
            <h2>🌐 Recommandations Haute Sévérité : Azure ({len(df_recommendations_azure)})</h2>
            <p>Recommandations critiques au niveau Azure (Subscriptions + Storage accounts) avec statut "Unassigned".</p>
        """
        
        if df_recommendations_azure.empty:
            html_content += "<div class='success-message'>✅ Aucune recommandation haute sévérité Azure non assignée trouvée.</div>"
        else:
            html_content += f"""
            <div class='info-box'>
                <h4>📊 Résumé Azure :</h4>
                <p><strong>{len(df_recommendations_azure)} types de recommandations</strong> concernant <strong>{total_affected_azure} ressources</strong> au total</p>
            </div>
            """
            
            # Tableau des recommandations Azure
            display_columns = ['recommendationName', 'category', 'affectedResources']
            df_display_azure = df_recommendations_azure[display_columns].rename(columns={
                'recommendationName': 'Recommandation',
                'category': 'Catégorie',
                'affectedResources': 'Ressources Affectées'
            })
            
            html_content += df_display_azure.to_html(index=False, border=0, classes='data-table', escape=False)

        html_content += "<br><hr><br>"

        # Section Recommandations machines haute sévérité
        html_content += f"""
            <h2>🚨 Recommandations Haute Sévérité : Machines ({len(df_recommendations_vms)})</h2>
            <p>Recommandations critiques avec statut "Unassigned" pour les machines virtuelles.</p>
        """
        
        if df_recommendations_vms.empty:
            html_content += "<div class='success-message'>✅ Aucune recommandation haute sévérité machines non assignée trouvée.</div>"
        else:
            html_content += f"""
            <div class='info-box'>
                <h4>📊 Résumé Machines :</h4>
                <p><strong>{len(df_recommendations_vms)} types de recommandations</strong> concernant <strong>{total_affected_vms} VMs</strong> au total</p>
            </div>
            """
            
            # Tableau des recommandations machines
            display_columns = ['recommendationName', 'category', 'affectedResources']
            df_display_vms = df_recommendations_vms[display_columns].rename(columns={
                'recommendationName': 'Recommandation',
                'category': 'Catégorie',
                'affectedResources': 'Ressources Affectées'
            })
            
            html_content += df_display_vms.to_html(index=False, border=0, classes='data-table', escape=False)

        html_content += "<br><hr><br>"
        
        # Section mises à jour en attente
        html_content += f"""
            <h2>🔄 Mises à jour en Attente ({len(df_pending)})</h2>
            <p>Machines virtuelles avec des mises à jour critiques ou de sécurité en attente.</p>
        """
        
        if df_pending.empty:
            html_content += "<div class='success-message'>✅ Aucune machine avec des mises à jour critiques ou de sécurité en attente.</div>"
        else:
            display_columns = ['vmName', 'osType', 'vmType', 'resourceGroup', 'securityCount']
            available_columns = [col for col in display_columns if col in df_pending.columns]
            
            df_display = df_pending[available_columns].rename(columns={
                'vmName': 'Nom de la VM',
                'osType': 'OS',
                'vmType': 'Type',
                'resourceGroup': 'Groupe de Ressources',
                'securityCount': 'Sécurité'
            })
            html_content += df_display.to_html(index=False, border=0, classes='data-table', escape=False)

        html_content += "<br><hr><br>"

        # Section machines sans données
        html_content += f"""
            <h2>⚠️ Machines sans Données de Patch ({len(df_no_data)})</h2>
            <p>Machines sans évaluation de correctifs valide.</p>
        """
        
        if df_no_data.empty:
            html_content += "<div class='success-message'>✅ Toutes les machines ont des données d'évaluation valides.</div>"
        else:
            display_columns = ['vmName', 'osType', 'vmType', 'resourceGroup', 'noDataReason']
            available_columns = [col for col in display_columns if col in df_no_data.columns]
            
            df_display = df_no_data[available_columns].rename(columns={
                'vmName': 'Nom de la VM',
                'osType': 'OS',
                'vmType': 'Type',
                'resourceGroup': 'Groupe de Ressources',
                'noDataReason': 'Raison'
            })
            html_content += df_display.to_html(index=False, border=0, classes='data-table', escape=False)

        # Template HTML avec CSS corrigé pour l'alignement
        html_template = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Azure Update Manager + Security Center - VERSION FINALE</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0; padding: 20px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }}
                .container {{
                    max-width: 1400px; margin: 0 auto; background: white;
                    border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                    padding: 40px;
                }}
                .header {{
                    text-align: center; padding-bottom: 30px;
                    border-bottom: 3px solid #0078d4; margin-bottom: 40px;
                }}
                .header h1 {{
                    color: #0078d4; font-size: 2.5em; margin: 0;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
                }}
                .header p {{ color: #666; margin-top: 10px; font-size: 1.1em; }}
                
                .stats-container {{
                    display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                    gap: 20px; margin-bottom: 40px;
                }}
                .stat-box {{
                    padding: 25px; border-radius: 10px; text-align: center;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: transform 0.3s;
                }}
                .stat-box:hover {{ transform: translateY(-5px); }}
                .stat-box.critical {{ background: linear-gradient(135deg, #ff6b6b, #ee5a52); color: white; }}
                .stat-box.warning {{ background: linear-gradient(135deg, #feca57, #ff9ff3); color: white; }}
                .stat-box.info {{ background: linear-gradient(135deg, #48cae4, #023e8a); color: white; }}
                .stat-box.secondary {{ background: linear-gradient(135deg, #6c5ce7, #a29bfe); color: white; }}
                .stat-box.success {{ background: linear-gradient(135deg, #20bf6b, #26a69a); color: white; }}
                .stat-box h3 {{ font-size: 2.2em; margin: 0; }}
                .stat-box p {{ margin: 10px 0 5px 0; font-size: 1.0em; }}
                .stat-box small {{ opacity: 0.8; font-size: 0.85em; }}
                
                .secure-score-detail {{
                    background: #f8f9fa; border-radius: 8px; padding: 20px; margin: 20px 0;
                    border-left: 4px solid #0078d4;
                }}
                .score-bar {{
                    height: 20px; background: #e9ecef; border-radius: 10px; overflow: hidden;
                    margin-top: 10px;
                }}
                .score-progress {{
                    height: 100%; background: linear-gradient(90deg, #20bf6b, #26a69a);
                    transition: width 0.3s ease;
                }}
                
                .info-box {{
                    background: #e3f2fd; border-left: 4px solid #2196f3;
                    padding: 15px 20px; margin: 20px 0; border-radius: 5px;
                }}
                .info-box h4 {{ margin: 0 0 10px 0; color: #1976d2; }}
                .info-box ul {{ margin: 0; }}
                .info-box li {{ margin: 5px 0; }}
                
                h2 {{ 
                    color: #0078d4; border-bottom: 2px solid #e3f2fd;
                    padding-bottom: 10px; margin-top: 40px; font-size: 1.8em;
                }}
                
                .data-table {{
                    width: 100%; border-collapse: collapse; margin-top: 20px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-radius: 8px;
                    overflow: hidden;
                }}
                .data-table th {{
                    background: linear-gradient(135deg, #0078d4, #106ebe);
                    color: white; 
                    padding: 15px 12px; 
                    font-weight: 600;
                    text-transform: uppercase; 
                    font-size: 0.85em;
                    text-align: left;
                    vertical-align: middle;
                }}
                .data-table td {{ 
                    padding: 12px; 
                    border-bottom: 1px solid #eee; 
                    font-size: 0.9em;
                    text-align: left;
                    vertical-align: middle;
                }}
                .data-table tr:nth-child(even) {{ background: #f8f9fa; }}
                .data-table tr:hover {{ background: #e3f2fd; }}
                
                .success-message {{
                    background: linear-gradient(135deg, #51cf66, #40c057);
                    color: white; padding: 15px 20px; border-radius: 8px;
                    margin: 20px 0; font-weight: 500; text-align: center;
                }}
                
                hr {{ 
                    border: none; height: 2px; 
                    background: linear-gradient(135deg, #0078d4, #106ebe); 
                    margin: 40px 0; opacity: 0.3;
                }}
                
                @media (max-width: 768px) {{
                    .stats-container {{ grid-template-columns: repeat(2, 1fr); }}
                    .data-table {{ font-size: 0.8em; }}
                    .data-table th, .data-table td {{ padding: 8px 5px; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔧 Azure Update Manager + Security Center</h1>
                    <p>Rapport Final avec Recommandations Azure • {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</p>
                </div>
                {html_content}
                <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; text-align: center; color: #666; font-size: 0.9em;">
                    <p>Rapport généré avec Azure Resource Graph + Microsoft Defender for Cloud<br>
                    Inclut: Machines • Azure (Subscriptions + Storage) • Secure Score • Update Manager</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html_template
    

    def run(self):
        """Exécute le processus complet."""
        try:
            subscription_id = self.get_subscription_id()
            
            print("\n🚀 Démarrage de l'analyse complète avec recommandations Azure...")
            
            # Récupération du Secure Score
            secure_score = self.get_azure_secure_score(subscription_id)
            
            # Récupération des recommandations machines avec filtre GA
            df_recommendations_vms = self.get_high_severity_machine_recommendations(subscription_id)
            
            # Récupération des recommandations Azure (nouveau)
            df_recommendations_azure = self.get_high_severity_azure_recommendations(subscription_id)
            
            # Traitement des données VM
            df_pending, df_no_data = self.process_vm_data(subscription_id)
            
            # Génération du rapport
            print("\n📄 Génération du rapport HTML final...")
            html_content = self.generate_complete_html_report(df_pending, df_no_data, secure_score, df_recommendations_vms, df_recommendations_azure)
            
            filename = f'azure_final_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"\n✅ Rapport généré avec succès: {filename}")
            print(f"📊 Résumé final:")
            if secure_score:
                print(f"   • Secure Score: {secure_score.get('percentage', 0)}%")
            print(f"   • Recommandations machines haute sévérité: {len(df_recommendations_vms)}")
            if not df_recommendations_vms.empty:
                total_vms = df_recommendations_vms['affectedCount'].sum()
                print(f"     → {total_vms} VMs concernées")
            print(f"   • Recommandations Azure haute sévérité: {len(df_recommendations_azure)}")
            if not df_recommendations_azure.empty:
                total_azure = df_recommendations_azure['affectedCount'].sum()
                print(f"     → {total_azure} ressources concernées")
            print(f"   • VMs avec mises à jour en attente: {len(df_pending)}")
            print(f"   • VMs sans données de patch: {len(df_no_data)}")
            print(f"\n🎯 Rapport avec recommandations Azure et Machines généré !")
            
        except KeyboardInterrupt:
            print("\n⚠️  Opération annulée par l'utilisateur")
        except Exception as e:
            print(f"\n❌ Erreur inattendue: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    reporter = AzureUpdateManagerFinal()
    reporter.run()