terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

provider "azurerm" {
  features {}
  skip_provider_registration = true
}

# 1. Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "pygame-resourcegroup"
  location = "East US" 
}

# 2. Azure Container Registry (ACR)
resource "azurerm_container_registry" "acr" {
  name                = "pygameacregistry${random_id.id.hex}" # Unique name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = true # Needed for CI/CD pipeline
}

# 3. Azure Kubernetes Service (AKS)
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "pygame-akservice"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "pygame-dns"

  default_node_pool {
    name       = "default"
    node_count = 1 
    vm_size    = "Standard_B2s" # Low-cost VM
  }

  identity {
    type = "SystemAssigned"
  }
  
  role_based_access_control_enabled = true
}

# Give AKS permission to pull from ACR
resource "azurerm_role_assignment" "aks_pull_acr" {
  scope                = azurerm_container_registry.acr.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_kubernetes_cluster.aks.identity[0].principal_id
}

# Random ID for unique ACR name
resource "random_id" "id" {
  byte_length = 6
}

# --- Outputs ---
output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}
output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.aks.name
}
output "acr_login_server" {
  value = azurerm_container_registry.acr.login_server
}
output "acr_name" {
  value = azurerm_container_registry.acr.name
}